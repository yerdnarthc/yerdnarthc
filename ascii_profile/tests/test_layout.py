import xml.etree.ElementTree as ET

import pytest

from ascii_converter.layout import (
	ADDITIONS_ACCENT,
	ANSI_COLORS,
	COLOR_BLOCK_HEIGHT,
	COLOR_BLOCK_WIDTH,
	DELETIONS_ACCENT,
	DETAILS_FOREGROUND,
	INFO_CHAR_WIDTH,
	INFO_FONT_SIZE,
	INFO_X,
	INFO_Y,
	LINE_HEIGHT,
	PORTRAIT_FONT_SIZE,
	PORTRAIT_X,
	PORTRAIT_Y,
	SECONDARY,
	additions_segment,
	build_profile_svg,
	build_profile_svg_from_portrait,
	deletions_segment,
	extract_portrait_svg,
	format_count,
	github_two_col_row,
	key_value,
	make_divider,
	render_profile_info,
	section_header,
)


def parse_fragment(fragment: str) -> list[ET.Element]:
	root = ET.fromstring(f"<root>{fragment}</root>")
	return list(root)


def test_make_divider_supports_custom_character_and_length():
	assert make_divider(".", 7) == "......."


def test_section_header_contains_title_and_divider():
	elements = parse_fragment(section_header(100, "GitHub Stats"))
	divider_text = elements[1].text

	assert elements[0].text == "GitHub Stats"
	assert elements[0].attrib["fill"] != elements[1].attrib["fill"]
	assert divider_text is not None
	assert divider_text == "------------"
	assert elements[1].attrib["x"] == elements[0].attrib["x"]
	assert float(elements[1].attrib["y"]) - float(elements[0].attrib["y"]) == LINE_HEIGHT


def test_key_value_flows_inline_without_leader_or_alignment():
	value = "Windows 11"
	elements = parse_fragment(key_value(100, "OS:", value))
	assert len(elements) == 1
	assert "".join(elements[0].itertext()) == "OS: Windows 11"
	assert elements[0][-1].attrib["fill"] == DETAILS_FOREGROUND
	assert elements[0].attrib["font-size"] == f"{INFO_FONT_SIZE}px"
	assert "textLength" not in elements[0].attrib
	assert all("x" not in segment.attrib for segment in elements[0])


def test_github_stats_row_uses_natural_inline_spacing():
	elements = parse_fragment(github_two_col_row(
		100,
		"Repos: ", [("95", "#ddd")],
		"Stars: ", [("342", "#ddd")],
	))
	assert len(elements) == 1
	assert "".join(elements[0].itertext()) == "Repos: 95 | Stars: 342"
	assert float(elements[0].attrib["x"]) == INFO_X


def test_format_count_groups_thousands():
	assert format_count(0) == "0"
	assert format_count(950) == "950"
	assert format_count(1000) == "1,000"
	assert format_count(10000) == "10,000"
	assert format_count(100000) == "100,000"
	assert format_count(1000000) == "1,000,000"
	assert format_count(2116) == "2,116"
	assert format_count(446276) == "446,276"


def test_additions_segment_is_green_with_plus_suffix():
	text, fill = additions_segment(523178)

	assert text == "523,178++"
	assert fill == ADDITIONS_ACCENT


def test_deletions_segment_is_red_with_minus_suffix():
	text, fill = deletions_segment(76902)

	assert text == "76,902--"
	assert fill == DELETIONS_ACCENT


def test_portrait_round_trip_preserves_artwork(test_profile, test_github_stats):
	# Full build embeds markers + portrait; extract + rebuild from the
	# fragment must keep the identical portrait while allowing fresh stats.
	full = build_profile_svg("@@", test_profile, test_github_stats)
	portrait = extract_portrait_svg(full)

	assert "@" in portrait

	rebuilt = build_profile_svg_from_portrait(portrait, test_profile, test_github_stats)

	assert extract_portrait_svg(rebuilt) == portrait
	assert "GitHub Stats" in rebuilt


def test_extract_portrait_fails_without_markers():
	with pytest.raises(RuntimeError, match="portrait markers"):
		extract_portrait_svg("<svg></svg>")


def test_profile_fields_have_no_blank_rows(test_profile, test_github_stats):
	elements = parse_fragment(render_profile_info(test_profile, test_github_stats))
	rows = {"".join(element.itertext()).split(":", 1)[0]: float(element.attrib["y"])
		for element in elements}
	assert rows["Languages.Programming"] - rows["Projects"] == LINE_HEIGHT
	assert rows["Hobbies.Software"] - rows["Languages.Real"] == LINE_HEIGHT


def test_automated_rebuild_restyles_legacy_portrait(test_profile, test_github_stats):
	legacy = '''<g transform="translate(1, 15)" fill="#E4C0A3"><g>
		<text x="0" y="13" font-size="13px"> </text>
		<text x="7" y="13" font-size="13px">&amp;</text>
		<text x="0" y="26" font-size="13px">@</text>
		<text x="7" y="26" font-size="13px"> </text>
	</g></g>'''
	rebuilt = build_profile_svg_from_portrait(legacy, test_profile, test_github_stats)
	assert rebuilt == build_profile_svg(" &\n@ ", test_profile, test_github_stats)
	portrait = ET.fromstring(extract_portrait_svg(rebuilt))
	assert portrait.attrib["transform"] == f"translate({PORTRAIT_X}, {PORTRAIT_Y})"
	glyphs = list(portrait.iter("text"))
	assert [glyph.text for glyph in glyphs] == [" ", "&", "@", " "]
	assert all(glyph.attrib["font-size"] == f"{PORTRAIT_FONT_SIZE}px" for glyph in glyphs)
	assert float(glyphs[0].attrib["y"]) + PORTRAIT_Y == INFO_Y


@pytest.mark.parametrize("ascii_art", ["@@", "@" * 80, "@\n" * 50, "\nA\n\nB", ""])
def test_repeated_updates_preserve_layout(ascii_art, test_profile, test_github_stats):
	original = build_profile_svg(ascii_art, test_profile, test_github_stats)
	rebuilt = original
	for _ in range(3):
		rebuilt = build_profile_svg_from_portrait(
			extract_portrait_svg(rebuilt), test_profile, test_github_stats,
		)
	assert rebuilt == original


def test_real_profile_and_large_metrics_fit_canvas(test_github_stats):
	from ascii_converter.profile_data import create_profile
	from dataclasses import replace

	stats = replace(test_github_stats, lines_of_code=10**12,
		lines_of_code_additions=10**12, lines_of_code_deletions=10**12)
	root = ET.fromstring(build_profile_svg("@\n" * 50, create_profile(), stats))
	width, height = float(root.attrib["width"]), float(root.attrib["height"])
	for element in root.findall("{http://www.w3.org/2000/svg}text"):
		assert float(element.attrib["x"]) + len("".join(element.itertext())) * INFO_CHAR_WIDTH < width
		assert float(element.attrib["y"]) < height
	assert height > 600


def test_profile_text_escapes_xml(test_profile, test_github_stats):
	from dataclasses import replace
	profile = replace(test_profile, host='A & B <C> "D"')
	elements = parse_fragment(render_profile_info(profile, test_github_stats))
	assert 'Host: A & B <C> "D"' in ["".join(element.itertext()) for element in elements]


def test_terminal_palette_sits_below_info_and_fits_canvas(test_profile, test_github_stats):
	root = ET.fromstring(build_profile_svg("@@", test_profile, test_github_stats))
	ns = "{http://www.w3.org/2000/svg}"
	palette = root.find(f"{ns}g[@id='terminal-colors']")
	assert palette is not None
	blocks = palette.findall(f"{ns}rect")
	assert [block.attrib["fill"] for block in blocks] == list(ANSI_COLORS)
	last_text_y = max(float(element.attrib["y"]) for element in root.findall(f"{ns}text"))
	for index, block in enumerate(blocks):
		assert float(block.attrib["x"]) == INFO_X + index % 8 * COLOR_BLOCK_WIDTH
		assert float(block.attrib["y"]) == last_text_y + LINE_HEIGHT + index // 8 * COLOR_BLOCK_HEIGHT
		assert float(block.attrib["x"]) + COLOR_BLOCK_WIDTH < float(root.attrib["width"])
		assert float(block.attrib["y"]) + COLOR_BLOCK_HEIGHT < float(root.attrib["height"])


