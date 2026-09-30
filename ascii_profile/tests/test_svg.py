# ascii_profile/tests/test_svg.py

import xml.etree.ElementTree as ET
import pytest
from ascii_converter.svg import ascii_to_svg

SVG_NAMESPACE = "{http://www.w3.org/2000/svg}"


def test_ascii_to_svg_is_valid_and_emits_one_text_element_per_character():
    svg = ascii_to_svg("A B\nCD", font_size=12, char_width=8)

    root = ET.fromstring(svg)
    text_elements = root.findall(f"{SVG_NAMESPACE}text")

    assert root.tag == f"{SVG_NAMESPACE}svg"
    assert root.attrib["width"] == "24"
    assert root.attrib["height"] == "24"
    assert [element.text for element in text_elements] == ["A", " ", "B", "C", "D"]
    assert [(element.attrib["x"], element.attrib["y"]) for element in text_elements] == [
        ("0", "12"),
        ("8", "12"),
        ("16", "12"),
        ("0", "24"),
        ("8", "24"),
    ]


def test_ascii_to_svg_escapes_xml_characters():
    svg = ascii_to_svg("<&>")

    root = ET.fromstring(svg)
    text_elements = root.findall(f"{SVG_NAMESPACE}text")

    assert [element.text for element in text_elements] == ["<", "&", ">"]


def test_ascii_to_svg_handles_empty_input():
    root = ET.fromstring(ascii_to_svg(""))

    assert root.attrib["width"] == "0"
    assert root.attrib["height"] == "0"
    assert root.findall(f"{SVG_NAMESPACE}text") == []


@pytest.mark.parametrize(
    "kwargs",
    [{"font_size": 0}, {"font_size": -1}, {"char_width": 0}, {"char_width": -1}],
)
def test_ascii_to_svg_rejects_non_positive_dimensions(kwargs):
    with pytest.raises(ValueError):
        ascii_to_svg("A", **kwargs)