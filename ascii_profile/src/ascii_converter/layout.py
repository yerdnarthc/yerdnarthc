# ascii_profile/src/ascii_converter/layout.py

from ascii_converter.profile import GitHubStats, Profile
from html import escape
from .svg import ascii_to_svg_group


# ============================================================
# CANVAS
# ============================================================

CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 530

BACKGROUND = "#0D1117"
PORTRAIT_FOREGROUND = "#E4C0A3"
DETAILS_FOREGROUND = "#DADDDF"
SECONDARY = "#8B949E"
ACCENT = "#E0B629"
BORDER = "#30363D"

# GitHub Stats value accents (GitHub Primer dark-mode palette).
# STAR_ACCENT matches the yellow/orange GitHub star icon,
# ADDITIONS/DELETIONS match diff ++ / -- colors.
STAR_ACCENT = "#E3B341"
ADDITIONS_ACCENT = "#3FB950"
DELETIONS_ACCENT = "#F85149"

SECTION_HEADER_ACCENT = "#EBDCD4"


# ============================================================
# ASCII PORTRAIT
# ============================================================

PORTRAIT_X = 1
PORTRAIT_Y = 15

PORTRAIT_FONT_SIZE = 13
PORTRAIT_CHAR_WIDTH = 7
PORTRAIT_FONT_FAMILY = "Consolas"

PORTRAIT_START_MARKER = "<!-- PORTRAIT_START -->"
PORTRAIT_END_MARKER = "<!-- PORTRAIT_END -->"


# ============================================================
# INFORMATION COLUMN
# ============================================================

INFO_X = 410
INFO_Y = 40

INFO_FONT_SIZE = 14
INFO_CHAR_WIDTH = 8
INFO_RIGHT_X = CANVAS_WIDTH - 30

KEY_LEADER_GAP = 0
LEADER_VALUE_GAP = 2

LINE_HEIGHT = 18
BULLET = "."
VALUE_LEADER = "......................"
DIVIDER_CHARACTER = "─"
DIVIDER_LENGTH = 73


def make_divider(character: str = DIVIDER_CHARACTER, length: int = DIVIDER_LENGTH) -> str:
    """Return a configurable horizontal divider for the profile header."""
    if len(character) != 1:
        raise ValueError("Divider character must contain exactly one character.")
    if length < 0:
        raise ValueError("Divider length must be non-negative.")

    return character * length


def section_header(
    y: float,
    title: str,
    x: float = INFO_X,
    end_x: float = CANVAS_WIDTH - 30,
    font_size: int = INFO_FONT_SIZE,
    char_width: int = INFO_CHAR_WIDTH,
    title_prefix: str = "- ",
    title_gap: int = 2,
    divider_character: str = DIVIDER_CHARACTER,
    section_header_accent: str = SECTION_HEADER_ACCENT,
) -> str:
    """Render a colored section title followed by a divider to ``end_x``."""
    title_text = f"{title_prefix}{title}"
    divider_x = x + len(title_text) * char_width + title_gap
    divider_length = max(0, int((end_x - divider_x) / char_width))

    return "\n".join([
        text_element(
            x,
            y,
            title_text,
            font_size=font_size,
            fill=section_header_accent,
        ),
        text_element(
            divider_x,
            y,
            make_divider(divider_character, divider_length),
            font_size=font_size,
            fill=SECONDARY,
        ),
    ])


def text_element(
    x: float,
    y: float,
    text: str,
    font_size: int = INFO_FONT_SIZE,
    fill: str = DETAILS_FOREGROUND,
    font_family: str = "Consolas",
    font_weight: str = "normal",
    letter_spacing: float = 0,
    text_length: float | None = None,
) -> str:
    text_length_attributes = ""
    if text_length is not None and text:
        text_length_attributes = (
            f' textLength="{text_length}" lengthAdjust="spacing"'
        )

    return (
        f'<text x="{x}" y="{y}" '
        f'font-family="{escape(font_family)}" '
        f'font-size="{font_size}px" '
        f'font-weight="{font_weight}" '
        f'letter-spacing="{letter_spacing}px" '
        f'{text_length_attributes} '
        f'fill="{fill}">'
        f'{escape(text)}'
        f'</text>'
    )


def colored_text_row(
    y: float,
    segments: list[tuple[str, str]],
    x: float = INFO_X,
    char_width: int = INFO_CHAR_WIDTH,
    right_x: float | None = None,
) -> str:
    """Render adjacent text segments with independent colors."""
    elements = []
    row_width = sum(len(text) * char_width for text, _ in segments)
    current_x = x if right_x is None else right_x - row_width

    for text, fill in segments:
        elements.append(text_element(
            current_x,
            y,
            text,
            fill=fill,
            text_length=len(text) * char_width,
        ))
        current_x += len(text) * char_width

    return "\n".join(elements)


def key_value(
    y: float,
    key: str,
    value: str,
    bullet: str = BULLET,
    value_leader: str = VALUE_LEADER,
    value_right_x: float | None = None,
) -> str:
    KEY_X = INFO_X
    value_right_edge = INFO_RIGHT_X if value_right_x is None else value_right_x
    key_text = f"{bullet} {key}"
    leader_x = KEY_X + len(key_text) * INFO_CHAR_WIDTH + KEY_LEADER_GAP
    value_column_x = value_right_edge - len(value) * INFO_CHAR_WIDTH
    leader_length = max(0, int(
        (value_column_x - leader_x - LEADER_VALUE_GAP) / INFO_CHAR_WIDTH
    ))
    leader = (value_leader * leader_length)[:leader_length]

    elements = [
        text_element(
            KEY_X,
            y,
            key_text,
            font_size=14,
            fill=ACCENT,
            text_length=len(key_text) * INFO_CHAR_WIDTH,
        ),
        text_element(
            value_column_x,
            y,
            value,
            font_size=14,
            fill=DETAILS_FOREGROUND,
            text_length=len(value) * INFO_CHAR_WIDTH,
        ),
    ]

    if leader:
        elements.insert(1, text_element(
            leader_x,
            y,
            leader,
            font_size=14,
            fill=SECONDARY,
            text_length=len(leader) * INFO_CHAR_WIDTH,
        ))

    return "\n".join(elements)


def github_stats_row(
    y: float,
    left_segments: list[tuple[str, str]],
    right_segments: list[tuple[str, str]] | None = None,
) -> str:
    """Render one right-aligned GitHub Stats row with a metric divider."""
    if right_segments is None:
        return colored_text_row(y, left_segments, right_x=INFO_RIGHT_X)

    return colored_text_row(
        y,
        [*left_segments, ("| ", SECONDARY), *right_segments],
        right_x=INFO_RIGHT_X,
    )


def segmented_text_element(
    x: float,
    y: float,
    segments: list[tuple[str, str]],
    font_size: int = INFO_FONT_SIZE,
    font_family: str = "Consolas",
) -> str:
    """Render multi-colored inline text as one <text> with <tspan>s.

    Why one element instead of one <text> per segment: each <text>
    with textLength + lengthAdjust="spacing" justifies on its own,
    so a tiny segment like "95 " spreads "9" and "5" apart to fill
    its width. One <text> justifies the whole value block once, so
    characters stay tight and colors just ride along in tspans.
    """
    total_width = sum(len(text) * INFO_CHAR_WIDTH for text, _ in segments)
    spans = "".join(
        f'<tspan fill="{fill}">{escape(text)}</tspan>'
        for text, fill in segments
    )

    return (
        f'<text x="{x}" y="{y}" '
        f'font-family="{escape(font_family)}" '
        f'font-size="{font_size}px" '
        f'font-weight="normal" '
        f'letter-spacing="0px" '
        f'textLength="{total_width}" lengthAdjust="spacing">'
        f'{spans}'
        f'</text>'
    )


def stat_field(
    y: float,
    key: str,
    value_segments: list[tuple[str, str]],
    col_x: float = INFO_X,
    col_right_x: float = INFO_RIGHT_X,
    value_leader: str = VALUE_LEADER,
    bullet: str | None = BULLET,
) -> str:
    """Render one `key .... value` metric inside a column.

    The key stays left-aligned at ``col_x`` and the (possibly
    multi-colored) value stays right-aligned at ``col_right_x``.
    Dots fill the gap, same style as ``key_value``.
    Pass ``bullet=None`` for continuation columns (Stars/Followers)
    that should not get a leading dot.
    """
    key_text = f"{bullet} {key}" if bullet else key
    value_width = sum(len(text) * INFO_CHAR_WIDTH for text, _ in value_segments)
    value_x = col_right_x - value_width
    key_x = col_x
    leader_x = key_x + len(key_text) * INFO_CHAR_WIDTH + KEY_LEADER_GAP
    leader_length = max(0, int(
        (value_x - leader_x - LEADER_VALUE_GAP) / INFO_CHAR_WIDTH
    ))
    leader = (value_leader * leader_length)[:leader_length]

    elements = [
        text_element(
            key_x,
            y,
            key_text,
            font_size=INFO_FONT_SIZE,
            fill=ACCENT,
            text_length=len(key_text) * INFO_CHAR_WIDTH,
        ),
    ]

    if leader:
        elements.append(text_element(
            leader_x,
            y,
            leader,
            font_size=INFO_FONT_SIZE,
            fill=SECONDARY,
            text_length=len(leader) * INFO_CHAR_WIDTH,
        ))

    # One <text> for the whole value block (see segmented_text_element):
    # keeps "95" tight instead of justifying each tiny segment alone.
    elements.append(segmented_text_element(value_x, y, value_segments))

    return "\n".join(elements)


# Single pipe with no embedded spaces: surrounding gaps are added
# explicitly via GITHUB_DIVIDER_GAP so left/right spacing is equal
# in coordinates. The old " | " baked spaces into the divider string,
# and lengthAdjust="spacing" then spread tracking unevenly around the
# narrow "|" glyph, which made the right side look wider.
GITHUB_DIVIDER = "|"
GITHUB_DIVIDER_GAP = INFO_CHAR_WIDTH


def github_two_col_row(
    y: float,
    left_key: str,
    left_value: list[tuple[str, str]],
    right_key: str,
    right_value: list[tuple[str, str]],
) -> str:
    """Render a GitHub Stats row with two dot-leader columns.

    Left column runs INFO_X -> middle divider, right column runs
    middle divider -> INFO_RIGHT_X. Both columns right-align their
    values, so `342` / `196` land on the same right edge while
    `. Repos:` / `. Commits:` share the same left edge.
    Only the left column gets a bullet; the right column
    (Stars/Followers) is a continuation without one.
    """
    mid_x = (INFO_X + INFO_RIGHT_X) / 2
    divider_width = len(GITHUB_DIVIDER) * INFO_CHAR_WIDTH
    divider_x = mid_x - divider_width / 2

    left_col_right = divider_x - GITHUB_DIVIDER_GAP
    right_col_x = divider_x + divider_width + GITHUB_DIVIDER_GAP

    return "\n".join([
        stat_field(y, left_key, left_value, INFO_X, left_col_right, bullet=BULLET),
        text_element(
            divider_x,
            y,
            GITHUB_DIVIDER,
            font_size=INFO_FONT_SIZE,
            fill=SECONDARY,
            text_length=divider_width,
        ),
        stat_field(y, right_key, right_value, right_col_x, INFO_RIGHT_X, bullet=None),
    ])


def github_full_row(
    y: float,
    key: str,
    value_segments: list[tuple[str, str]],
    bullet: str | None = BULLET,
) -> str:
    """Render a full-width GitHub Stats row (used for Lines of Code)."""
    return stat_field(y, key, value_segments, INFO_X, INFO_RIGHT_X, bullet=bullet)


def join_items(items: list[str]) -> str:
    return ", ".join(items)


def format_count(value: int) -> str:
    """Format a GitHub Stats number with thousands separators.

    950 -> "950", 2116 -> "2,116", 446276 -> "446,276".
    Uses Python's `:,` format spec (comma grouping).
    """
    if not isinstance(value, int):
        raise TypeError("GitHub Stats count must be an int.")
    if value < 0:
        raise ValueError("GitHub Stats count must be non-negative.")
    return f"{value:,}"


def additions_segment(value: int) -> tuple[str, str]:
    """Style a lines-added value: green text with `++` suffix."""
    return (f"{format_count(value)}++", ADDITIONS_ACCENT)


def deletions_segment(value: int) -> tuple[str, str]:
    """Style a lines-removed value: red text with `--` suffix."""
    return (f"{format_count(value)}--", DELETIONS_ACCENT)


def render_profile_info(
        profile: Profile,
        github_stats: GitHubStats
    ) -> str:
    elements = []

    # Profile username at the top of the info column, bold and accented
    elements.append(
        text_element(
            INFO_X,
            INFO_Y,
            profile.username,
            font_size=16,
            fill=ACCENT,
            font_weight="bold",
        )
    )

    DIVIDER_MARGIN_TOP = 20
    DIVIDER_MARGIN_BOTTOM = 20

    # Add some vertical space after the username
    y = INFO_Y + DIVIDER_MARGIN_TOP

    elements.append(
        text_element(
            INFO_X,
            y,
            make_divider(),
            font_size=14,
            fill=SECONDARY,
        )
    )

    y += DIVIDER_MARGIN_BOTTOM

    # OS Label
    elements.append(
        key_value(
            y, 
            "OS:", 
            profile.operating_system
        ))
    y += LINE_HEIGHT

    # Uptime Label
    # Hardcoded for now, but could be dynamically generated in the future
    elements.append(
        key_value(
            y, 
            "Uptime:", 
            profile.uptime
        ))
    y += LINE_HEIGHT

    # Host Label
    elements.append(
        key_value(
            y, 
            "Host:", 
            profile.host
        ))
    y += LINE_HEIGHT

    # Kernel Label
    elements.append(
        key_value(
            y, 
            "Kernel:", 
            profile.kernel
        ))
    y += LINE_HEIGHT

    # IDE Label
    elements.append(key_value(
        y,
        "IDE:",
        profile.ide,
    ))
    y += LINE_HEIGHT

    # Projects Label
    elements.append(key_value(
        y, 
        "Projects:", 
        join_items(profile.projects)
    ))
    y += LINE_HEIGHT

    # Newline before the Languages section
    y += LINE_HEIGHT

    # Programming Languages Label
    elements.append(key_value(
        y,
        "Languages.Programming:",
        join_items(profile.programming_languages),
    ))
    y += LINE_HEIGHT

    # Other Languages Label
    elements.append(key_value(
        y,
        "Languages.Other:",
        join_items(profile.other_languages),
    ))
    y += LINE_HEIGHT

    # Real Languages Label
    elements.append(key_value(
        y,
        "Languages.Real:",
        join_items(profile.real_languages),
    ))
    y += LINE_HEIGHT

    # Newline before the Hobbies section
    y += LINE_HEIGHT

    # Software Hobbies Label
    elements.append(key_value(
        y,
        "Hobbies.Software:",
        join_items(profile.software_hobbies),
    ))
    y += LINE_HEIGHT

    # Hardware Hobbies Label
    elements.append(key_value(
        y,
        "Hobbies.Hardware:",
        join_items(profile.hardware_hobbies),
    ))
    y += LINE_HEIGHT

    # Newline before the Contacts section
    y += LINE_HEIGHT

    # Contacts section header
    elements.append(
        section_header(
            y, 
            "Contacts", 
            title_prefix="- ", 
            title_gap=5, 
            end_x=CANVAS_WIDTH - 5,
        )
    )
    y += LINE_HEIGHT

    # Personal Email Label
    elements.append(
        key_value(
            y,
            "Email.Personal:",
            profile.email_personal,
        )
    )
    y += LINE_HEIGHT

    # Institutional Email Label
    elements.append(
        key_value(
            y,
            "Email.Institutional:",
            profile.email_institutional,
        )
    )
    y += LINE_HEIGHT

    # LinkedIn Label
    elements.append(
        key_value(
            y,
            "LinkedIn:",
            profile.linkedin,
        )
    )
    y += LINE_HEIGHT

    # Discord Label
    elements.append(
        key_value(
            y,
            "Discord:",
            profile.discord,
        )
    )
    y += LINE_HEIGHT

    # Newline before the GitHub Stats section
    y += LINE_HEIGHT

    # GitHub Stats section header
    elements.append(
        section_header(
            y, 
            "GitHub Stats", 
            title_prefix="- ", 
            title_gap=5, 
            end_x=CANVAS_WIDTH - 5,
        )
    )
    y += LINE_HEIGHT

    # GitHub Stats row 1: Contains Repos and Stars with a divider
    elements.append(github_two_col_row(
        y,
        "Repos: ",
        [
            (f"{format_count(github_stats.repositories)} ", DETAILS_FOREGROUND),
            ("{", SECONDARY),
            ("Contributed: ", ACCENT),
            (format_count(github_stats.contributions), DETAILS_FOREGROUND),
            ("}", SECONDARY),
        ],
        "Stars: ",
        [
            (format_count(github_stats.stars), STAR_ACCENT),
        ],
    ))
    y += LINE_HEIGHT

    # GitHub Stats row 2: Contains Commits and Followers with a divider
    elements.append(github_two_col_row(
        y,
        "Commits: ",
        [
            (format_count(github_stats.commits), DETAILS_FOREGROUND),
        ],
        "Followers: ",
        [
            (format_count(github_stats.followers), DETAILS_FOREGROUND),
        ],
    ))
    y += LINE_HEIGHT

    # GitHub Stats row 3: Contains Lines of Code with additions and deletions
    elements.append(github_full_row(
        y,
        "Lines of Code on GitHub: ",
        [
            (f"{format_count(github_stats.lines_of_code)} ", DETAILS_FOREGROUND),
            ("(", SECONDARY),
            additions_segment(github_stats.lines_of_code_additions),
            (", ", SECONDARY),
            deletions_segment(github_stats.lines_of_code_deletions),
            (")", SECONDARY),
        ],
    ))


    return "\n".join(elements)


def build_profile_svg(
        ascii_art: str,
        profile: Profile,
        github_stats: GitHubStats,
    ) -> str:
    """
    Convert ASCII art and profile data into a complete SVG.
    Used for the local/full generation (portrait image available).
    """

    portrait_inner = ascii_to_svg_group(
        ascii_art,
        font_size=PORTRAIT_FONT_SIZE,
        font_family=PORTRAIT_FONT_FAMILY,
        char_width=PORTRAIT_CHAR_WIDTH,
    )
    portrait_svg = render_portrait_group(portrait_inner)

    return _build_profile_svg(
        portrait_svg,
        profile,
        github_stats,
    )


def build_profile_svg_from_portrait(
        portrait_svg: str,
        profile: Profile,
        github_stats: GitHubStats,
    ) -> str:
    """
    Build a complete SVG using an already-rendered portrait fragment.

    Used by the automated GitHub Actions update, where the original
    portrait image is unavailable. The portrait is read from the
    previously committed profile.svg via extract_portrait_svg().
    """

    return _build_profile_svg(
        portrait_svg,
        profile,
        github_stats,
    )


def extract_portrait_svg(svg: str) -> str:
    """
    Extract the portrait SVG group from an existing profile SVG.

    Looks for the PORTRAIT_START / PORTRAIT_END markers written by
    _build_profile_svg() and returns everything between them.
    """

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
    """Wrap rendered ASCII in the positioned outer portrait group.

    Kept separate so the local build and the Actions rebuild share the
    exact same wrapper. extract_portrait_svg() returns this whole block,
    and _build_profile_svg() inserts it verbatim (no second wrapper),
    which keeps extract -> rebuild idempotent.
    """
    return (
        f'<g transform="translate({PORTRAIT_X}, {PORTRAIT_Y})"\n'
        f'     fill="{PORTRAIT_FOREGROUND}">\n'
        f'    {portrait_inner}\n'
        f'</g>'
    )


def _build_profile_svg(
        portrait_svg: str,
        profile: Profile,
        github_stats: GitHubStats,
    ) -> str:
    """
    Build the complete neofetch-style profile SVG
    using an already-rendered portrait SVG group.
    """

    svg = f'''<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{CANVAS_WIDTH}"
    height="{CANVAS_HEIGHT}"
    viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}"
>

    <rect
        width="100%"
        height="100%"
        rx="16"
        fill="{BACKGROUND}"
        stroke="{BORDER}"
    />

    {PORTRAIT_START_MARKER}
    {portrait_svg}
    {PORTRAIT_END_MARKER}

    {render_profile_info(profile, github_stats)}

</svg>'''

    return svg