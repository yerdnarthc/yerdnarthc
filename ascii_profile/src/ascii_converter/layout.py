"""Shared neofetch-style SVG layout for local and automated generation."""

from html import escape
from math import ceil
import xml.etree.ElementTree as ET

from .profile import GitHubStats, Profile
from .svg import ascii_to_svg_group


CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 630
PADDING = 30
COLUMN_GAP = 50

BACKGROUND = "#101313"
PORTRAIT_FOREGROUND = "#34FFE4"
DETAILS_FOREGROUND = "#DADDDF"
SECONDARY = "#8B949E"
ACCENT = "#34FFE4"
BORDER = "#30363D"
STAR_ACCENT = "#E3B341"
ADDITIONS_ACCENT = "#3EEB55"
DELETIONS_ACCENT = "#F85149"
SECTION_HEADER_ACCENT = "#EBDCD4"

FONT_FAMILY = "Consolas, 'Liberation Mono', monospace"
INFO_X = 460
INFO_Y = 55
INFO_FONT_SIZE = 16
INFO_CHAR_WIDTH = INFO_FONT_SIZE * 0.6
LINE_HEIGHT = 19

PORTRAIT_FONT_SIZE = 15
PORTRAIT_CHAR_WIDTH = 7.5
PORTRAIT_FONT_FAMILY = FONT_FAMILY
PORTRAIT_X = PADDING
# The first glyph baseline matches the username baseline.
PORTRAIT_Y = INFO_Y - PORTRAIT_FONT_SIZE
PORTRAIT_START_MARKER = "<!-- PORTRAIT_START -->"
PORTRAIT_END_MARKER = "<!-- PORTRAIT_END -->"

DIVIDER_CHARACTER = "-"
DIVIDER_LENGTH = 10

# ANSI order: black, red, green, yellow, blue, magenta, cyan, white;
# followed by the bright variants. These swatches complement the profile theme.
ANSI_COLORS = (
    "#242929", DELETIONS_ACCENT, ADDITIONS_ACCENT, STAR_ACCENT,
    "#58A6FF", "#BC8CFF", ACCENT, DETAILS_FOREGROUND,
    "#636D70", "#FF7B72", "#7EE787", "#F2CC60",
    "#79C0FF", "#D2A8FF", "#85FFEF", "#FFFFFF",
)
COLOR_BLOCK_WIDTH = 24
COLOR_BLOCK_HEIGHT = 16
COLOR_BLOCK_COLUMNS = 8


def render_color_blocks(y: float) -> str:
    """Show the normal and bright ANSI palettes as two contiguous rows."""
    blocks = [
        '<g id="terminal-colors" role="img" aria-label="ANSI terminal color palette">',
        '<title>ANSI terminal colors: standard and bright</title>',
    ]
    for index, color in enumerate(ANSI_COLORS):
        x = INFO_X + (index % COLOR_BLOCK_COLUMNS) * COLOR_BLOCK_WIDTH
        block_y = y + (index // COLOR_BLOCK_COLUMNS) * COLOR_BLOCK_HEIGHT
        blocks.append(
            f'<rect x="{x}" y="{block_y}" width="{COLOR_BLOCK_WIDTH}" '
            f'height="{COLOR_BLOCK_HEIGHT}" fill="{color}" />'
        )
    blocks.append('</g>')
    return "\n".join(blocks)


def make_divider(character: str = DIVIDER_CHARACTER, length: int = DIVIDER_LENGTH) -> str:
    """Return a short ASCII divider, normally as wide as its heading."""
    if len(character) != 1:
        raise ValueError("Divider character must contain exactly one character.")
    if length < 0:
        raise ValueError("Divider length must be non-negative.")
    return character * length


def text_element(
    x: float,
    y: float,
    text: str,
    font_size: int = INFO_FONT_SIZE,
    fill: str = DETAILS_FOREGROUND,
    font_family: str = FONT_FAMILY,
    font_weight: str = "normal",
) -> str:
    return (
        f'<text x="{x}" y="{y}" '
        f'font-family="{escape(font_family, quote=True)}" '
        f'font-size="{font_size}px" font-weight="{font_weight}" '
        f'xml:space="preserve" fill="{fill}">{escape(text)}</text>'
    )


def section_header(
    y: float,
    title: str,
    fill: str = SECTION_HEADER_ACCENT,
) -> str:
    """Put a heading-sized row of hyphens beneath the heading."""
    return "\n".join([
        text_element(INFO_X, y, title, fill=fill, font_weight="bold"),
        text_element(
            INFO_X, y + LINE_HEIGHT, make_divider(length=len(title)), fill=SECONDARY,
        ),
    ])


def segmented_text_element(
    x: float,
    y: float,
    segments: list[tuple[str, str]],
) -> str:
    """Keep colored segments in natural inline flow, including spaces."""
    spans = "".join(
        f'<tspan fill="{fill}">{escape(text)}</tspan>'
        for text, fill in segments
    )
    return (
        f'<text x="{x}" y="{y}" '
        f'font-family="{escape(FONT_FAMILY, quote=True)}" '
        f'font-size="{INFO_FONT_SIZE}px" xml:space="preserve">{spans}</text>'
    )


def key_value(y: float, key: str, value: str) -> str:
    """Render Key: value with exactly one space after the colon."""
    return stat_field(y, key, [(value, DETAILS_FOREGROUND)])


def stat_field(
    y: float,
    key: str,
    value_segments: list[tuple[str, str]],
) -> str:
    return segmented_text_element(
        INFO_X, y, [(f"{key.rstrip()} ", ACCENT), *value_segments],
    )


def github_two_col_row(
    y: float,
    left_key: str,
    left_value: list[tuple[str, str]],
    right_key: str,
    right_value: list[tuple[str, str]],
) -> str:
    """Keep paired metrics adjacent, separated by a spaced pipe."""
    return stat_field(y, left_key, [
        *left_value,
        (" | ", SECONDARY),
        (f"{right_key.rstrip()} ", ACCENT),
        *right_value,
    ])


def join_items(items: list[str]) -> str:
    return ", ".join(items)


def format_count(value: int) -> str:
    """Format a non-negative GitHub metric with thousands separators."""
    if not isinstance(value, int):
        raise TypeError("GitHub Stats count must be an int.")
    if value < 0:
        raise ValueError("GitHub Stats count must be non-negative.")
    return f"{value:,}"


def additions_segment(value: int) -> tuple[str, str]:
    return (f"{format_count(value)}++", ADDITIONS_ACCENT)


def deletions_segment(value: int) -> tuple[str, str]:
    return (f"{format_count(value)}--", DELETIONS_ACCENT)


def render_profile_info(profile: Profile, github_stats: GitHubStats) -> str:
    elements = [section_header(INFO_Y, profile.username, fill=ACCENT)]
    y = INFO_Y + 2 * LINE_HEIGHT

    fields = [
        ("OS:", profile.operating_system),
        ("Uptime:", profile.uptime),
        ("Host:", profile.host),
        ("Kernel:", profile.kernel),
        ("IDE:", profile.ide),
        ("Projects:", join_items(profile.projects)),
        ("Languages.Programming:", join_items(profile.programming_languages)),
        ("Languages.Other:", join_items(profile.other_languages)),
        ("Languages.Real:", join_items(profile.real_languages)),
        ("Hobbies.Software:", join_items(profile.software_hobbies)),
        ("Hobbies.Hardware:", join_items(profile.hardware_hobbies)),
    ]
    for key, value in fields:
        elements.append(key_value(y, key, value))
        y += LINE_HEIGHT

    y += LINE_HEIGHT
    elements.append(section_header(y, "Contacts"))
    y += 2 * LINE_HEIGHT
    contacts = [
        ("Email.Personal:", profile.email_personal),
        ("Email.Institutional:", profile.email_institutional),
        ("LinkedIn:", profile.linkedin),
        ("Discord:", profile.discord),
    ]
    for key, value in contacts:
        elements.append(key_value(y, key, value))
        y += LINE_HEIGHT

    y += LINE_HEIGHT
    elements.append(section_header(y, "GitHub Stats"))
    y += 2 * LINE_HEIGHT
    elements.append(github_two_col_row(
        y,
        "Repos:",
        [
            (f"{format_count(github_stats.repositories)} ", DETAILS_FOREGROUND),
            ("{", SECONDARY),
            ("Contributed: ", ACCENT),
            (format_count(github_stats.contributions), DETAILS_FOREGROUND),
            ("}", SECONDARY),
        ],
        "Stars:",
        [(format_count(github_stats.stars), STAR_ACCENT)],
    ))
    y += LINE_HEIGHT
    elements.append(github_two_col_row(
        y,
        "Commits:",
        [(format_count(github_stats.commits), DETAILS_FOREGROUND)],
        "Followers:",
        [(format_count(github_stats.followers), DETAILS_FOREGROUND)],
    ))
    y += LINE_HEIGHT
    elements.append(stat_field(y, "Lines Changed on GitHub:", [
        (f"{format_count(github_stats.lines_of_code)} ", DETAILS_FOREGROUND),
        ("(", SECONDARY),
        additions_segment(github_stats.lines_of_code_additions),
        (", ", SECONDARY),
        deletions_segment(github_stats.lines_of_code_deletions),
        (")", SECONDARY),
    ]))
    return "\n".join(elements)


def build_profile_svg(ascii_art: str, profile: Profile, github_stats: GitHubStats) -> str:
    """Build the local profile from ASCII art and current profile data."""
    portrait_inner = ascii_to_svg_group(
        ascii_art,
        font_size=PORTRAIT_FONT_SIZE,
        font_family=PORTRAIT_FONT_FAMILY,
        char_width=PORTRAIT_CHAR_WIDTH,
    )
    return _build_profile_svg(render_portrait_group(portrait_inner), profile, github_stats)


def build_profile_svg_from_portrait(
    portrait_svg: str,
    profile: Profile,
    github_stats: GitHubStats,
) -> str:
    """Restyle the embedded character grid without needing the source image.

    Older SVGs retain their original font sizes and translations. Recovering
    their per-character ASCII rows lets Actions apply the current layout
    exactly once, just like local generation, without accumulating transforms.
    """
    root = ET.fromstring(portrait_svg)
    rows: dict[int, list[tuple[float, str]]] = {}
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] == "text":
            x = float(element.attrib["x"])
            y = float(element.attrib["y"])
            row_height = float(element.attrib["font-size"].removesuffix("px"))
            row_index = round(y / row_height) - 1
            rows.setdefault(row_index, []).append((x, element.text or ""))
    ascii_art = "\n".join(
        "".join(character for _, character in sorted(rows.get(row_index, [])))
        for row_index in range(max(rows, default=-1) + 1)
    )
    return build_profile_svg(ascii_art, profile, github_stats)


def extract_portrait_svg(svg: str) -> str:
    """Extract the embedded portrait used by the automated updater."""
    try:
        start = svg.index(PORTRAIT_START_MARKER) + len(PORTRAIT_START_MARKER)
        end = svg.index(PORTRAIT_END_MARKER)
    except ValueError as exc:
        raise RuntimeError(
            "Could not find portrait markers in profile.svg. "
            "Regenerate it locally with main.py first."
        ) from exc
    return svg[start:end].strip()


def render_portrait_group(portrait_inner: str) -> str:
    return (
        f'<g transform="translate({PORTRAIT_X}, {PORTRAIT_Y})" '
        f'fill="{PORTRAIT_FOREGROUND}">\n{portrait_inner}\n</g>'
    )


def _build_profile_svg(portrait_svg: str, profile: Profile, github_stats: GitHubStats) -> str:
    info_svg = render_profile_info(profile, github_stats)
    # Growing metrics and longer profile fields expand the canvas rather than
    # shrinking the font. Retain the existing canvas as the minimum size.
    info_elements = list(ET.fromstring(f"<g>{info_svg}</g>"))
    info_bottom = max(float(element.attrib["y"]) for element in info_elements)
    palette_y = info_bottom + LINE_HEIGHT
    info_right = max(
        (INFO_X + len("".join(element.itertext())) * INFO_CHAR_WIDTH for element in info_elements),
        default=INFO_X,
    )
    portrait_root = ET.fromstring(portrait_svg)
    glyphs = list(portrait_root.iter("text"))
    portrait_right = max(
        (float(glyph.attrib["x"]) + PORTRAIT_CHAR_WIDTH for glyph in glyphs), default=0,
    )
    portrait_bottom = max((float(glyph.attrib["y"]) for glyph in glyphs), default=0)
    # Keep the portrait proportional if a wider ASCII grid is supplied.
    available_width = INFO_X - PORTRAIT_X - COLUMN_GAP
    portrait_scale = min(1, available_width / portrait_right) if portrait_right else 1
    if portrait_scale < 1:
        portrait_root.set(
            "transform",
            f"translate({PORTRAIT_X}, {INFO_Y - PORTRAIT_FONT_SIZE * portrait_scale}) "
            f"scale({portrait_scale})",
        )
        portrait_svg = ET.tostring(portrait_root, encoding="unicode")
    width = max(
        CANVAS_WIDTH, ceil(info_right + PADDING),
        INFO_X + COLOR_BLOCK_COLUMNS * COLOR_BLOCK_WIDTH + PADDING,
    )
    height = max(
        CANVAS_HEIGHT,
        ceil(palette_y + 2 * COLOR_BLOCK_HEIGHT + PADDING),
        ceil(INFO_Y + (portrait_bottom - PORTRAIT_FONT_SIZE) * portrait_scale + PADDING),
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <rect width="100%" height="100%" rx="16" fill="{BACKGROUND}" stroke="{BORDER}" />
    {PORTRAIT_START_MARKER}
    {portrait_svg}
    {PORTRAIT_END_MARKER}
    {info_svg}
    {render_color_blocks(palette_y)}
</svg>'''
