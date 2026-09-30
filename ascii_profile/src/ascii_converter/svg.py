# ascii_profile/src/ascii_converter/svg.py

from html import escape
from base64 import b64encode
from pathlib import Path


def embed_font(font_path: str, font_family: str) -> str:
    path = Path(font_path)
    font_data = b64encode(path.read_bytes()).decode("ascii")

    formats = {
        ".ttf": ("font/ttf", "truetype"),
        ".otf": ("font/otf", "opentype"),
        ".woff": ("font/woff", "woff"),
        ".woff2": ("font/woff2", "woff2"),
    }

    mime_type, font_format = formats[path.suffix.lower()]

    return (
        "@font-face {"
        f"font-family: '{escape(font_family)}';"
        f"src: url('data:{mime_type};base64,{font_data}') "
        f"format('{font_format}');"
        "}"
    )


def ascii_to_svg(
    ascii_art: str,
    font_size: int = 10,
    font_family: str = "monospace",
    char_width: float | None = None,
    font_path: str | None = None,
) -> str:
    """Convert ASCII art to a standalone SVG with one text element per character."""
    if font_size <= 0:
        raise ValueError("font_size must be greater than 0.")

    if char_width is None:
        char_width = font_size
    elif char_width <= 0:
        raise ValueError("char_width must be greater than 0.")

    lines = ascii_art.splitlines()
    width = max((len(line) for line in lines), default=0)
    height = len(lines)

    if font_path is not None:
        font_css = embed_font(font_path, font_family)
    else:
        font_css = ""

    svg_lines = [
        (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{width * char_width}" height="{height * font_size}" '
            'xml:space="preserve">'
        ),
        (
            f"<style>{font_css}"
            f"text {{ font-family: '{escape(font_family, quote=True)}'; "
            f"font-size: {font_size}px; }}</style>"
        ),
    ]

    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            svg_lines.append(
                f'<text x="{x * char_width}" y="{(y + 1) * font_size}">'
                f"{escape(character)}"
                "</text>"
            )

    svg_lines.append("</svg>")
    return "\n".join(svg_lines)


def ascii_to_svg_group(
    ascii_art: str,
    font_size: int = 10,
    font_family: str = "monospace",
    char_width: float | None = None,
) -> str:
    """Render ASCII art as an SVG <g> element."""

    if font_size <= 0:
        raise ValueError("font_size must be greater than 0.")

    if char_width is None:
        char_width = font_size

    if char_width <= 0:
        raise ValueError("char_width must be greater than 0.")

    lines = ascii_art.splitlines()

    svg_lines = [
        "<g>",
    ]

    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            svg_lines.append(
                f'<text '
                f'x="{x * char_width}" '
                f'y="{(y + 1) * font_size}" '
                f'font-family="{escape(font_family, quote=True)}" '
                f'font-size="{font_size}px">'
                f"{escape(character)}"
                f"</text>"
            )

    svg_lines.append("</g>")

    return "\n".join(svg_lines)