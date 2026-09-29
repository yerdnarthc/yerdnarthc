# ascii_profile/tests/test_mapping.py

from ascii_converter.mapping import pixel_to_char
from ascii_converter.mapping import make_checkerboard
from ascii_converter.mapping import checkerboard_to_ascii
from ascii_converter.mapping import make_three_tone_checkerboard
from ascii_converter.mapping import three_tone_checkerboard_to_ascii


def test_black_pixel():
    assert pixel_to_char(0) == " "


def test_white_pixel():
    assert pixel_to_char(255) == "@"


def test_mid_gray_pixel():
    assert pixel_to_char(128) == "+"


def test_invalid_pixel_value_low():
    try:
        pixel_to_char(-1)
    except ValueError as e:
        assert str(e) == "Pixel value must be between 0 and 255."


def test_invalid_pixel_value_high():
    try:
        pixel_to_char(256)
    except ValueError as e:
        assert str(e) == "Pixel value must be between 0 and 255."


def test_checkerboard_pattern():
    width, height = 4, 4
    checkerboard_image = make_checkerboard(width, height)
    pixels = list(checkerboard_image.get_flattened_data())

    expected_pixels = [
        0, 255, 0, 255,
        255, 0, 255, 0,
        0, 255, 0, 255,
        255, 0, 255, 0
    ]

    assert pixels == expected_pixels


def test_three_tone_checkerboard():
    width, height = 5, 5
    three_tone_checkerboard = make_three_tone_checkerboard(width, height)
    pixels = list(three_tone_checkerboard.get_flattened_data())

    expected_pixels = [
        0, 128, 255, 0, 128,
        255, 0, 128, 255, 0,
        128, 255, 0, 128, 255,
        0, 128, 255, 0, 128,
        255, 0, 128, 255, 0
    ]

    assert pixels == expected_pixels
    

def test_checkerboard_to_ascii():
    width, height = 4, 4
    checkerboard = make_checkerboard(width, height)
    ascii_art = checkerboard_to_ascii(checkerboard)

    expected_ascii_art = [
        " @ @",
        "@ @ ",
        " @ @",
        "@ @ "
    ]

    assert ascii_art == expected_ascii_art


def test_three_tone_checkerboard_to_ascii():
    width, height = 5, 5
    three_tone_checkerboard = make_three_tone_checkerboard(width, height)
    ascii_art = three_tone_checkerboard_to_ascii(three_tone_checkerboard)

    expected_ascii_art = [
        " +@ +",
        "@ +@ ",
        "+@ +@",
        " +@ +",
        "@ +@ "
    ]

    assert ascii_art == expected_ascii_art


