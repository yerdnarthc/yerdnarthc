import xml.etree.ElementTree as ET

from ascii_converter.layout import (
	DETAILS_FOREGROUND,
	INFO_CHAR_WIDTH,
	INFO_RIGHT_X,
	SECONDARY,
	build_profile_svg,
	colored_text_row,
	github_stats_row,
	key_value,
	make_divider,
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

	assert elements[0].text == "- GitHub Stats"
	assert elements[0].attrib["fill"] != elements[1].attrib["fill"]
	assert divider_text is not None
	assert set(divider_text) == {"─"}


def test_key_value_right_aligns_value_and_leader():
	value = "Windows 11"
	elements = parse_fragment(key_value(100, "OS:", value))
	value_element = elements[-1]
	leader_element = elements[1]

	expected_value_x = INFO_RIGHT_X - len(value) * INFO_CHAR_WIDTH

	assert int(value_element.attrib["x"]) == expected_value_x
	assert int(value_element.attrib["x"]) + len(value) * INFO_CHAR_WIDTH == INFO_RIGHT_X
	assert leader_element.text
	assert int(leader_element.attrib["x"]) > int(elements[0].attrib["x"])
	assert value_element.attrib["fill"] == DETAILS_FOREGROUND
	assert leader_element.attrib["fill"] == SECONDARY


def test_colored_text_row_right_aligns_complete_row():
	segments = [("Repos: ", "#fff"), ("95", "#ddd"), (" | Stars: ", "#aaa"), ("342", "#ddd")]
	elements = parse_fragment(colored_text_row(100, segments, right_x=INFO_RIGHT_X))
	rendered_width = sum(len(text) * INFO_CHAR_WIDTH for text, _ in segments)

	assert int(elements[0].attrib["x"]) == INFO_RIGHT_X - rendered_width
	assert int(elements[-1].attrib["x"]) + len(segments[-1][0]) * INFO_CHAR_WIDTH == INFO_RIGHT_X
	assert [element.text for element in elements] == [text for text, _ in segments]


def test_github_stats_row_separates_columns_and_aligns_right_value():
	elements = parse_fragment(github_stats_row(
		100,
		[("Repos: ", "#fff"), ("95 ", "#ddd")],
		[("Stars: ", "#fff"), ("342", "#ddd")],
	))
	rendered_text = [element.text for element in elements]
	stars_value = elements[-1]

	assert "| " in rendered_text
	assert rendered_text[0] == "Repos: "
	assert rendered_text[-2:] == ["Stars: ", "342"]
	assert int(stars_value.attrib["x"]) + int(stars_value.attrib["textLength"]) == INFO_RIGHT_X


# def test_profile_svg_contains_github_stats_section():
# 	root = ET.fromstring(build_profile_svg("@@"))
# 	svg_text = "".join(root.itertext())

# 	assert "GitHub Stats" in svg_text
# 	assert "Repos: " in svg_text
# 	assert "446,276" in svg_text
# 	assert "76,902--" in svg_text



