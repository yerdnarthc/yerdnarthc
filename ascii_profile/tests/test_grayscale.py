# ascii_profile/tests/test_grayscale.py

import pytest
from PIL import Image

from ascii_converter.grayscale import convert_to_grayscale


def test_convert_to_grayscale_returns_grayscale_image():
    image = Image.new("RGB", (2, 1), color=(255, 0, 0))

    grayscale_image = convert_to_grayscale(image)

    assert grayscale_image.mode == "L"
    assert grayscale_image.size == image.size


def test_contrast_increases_tonal_separation():
    image = Image.new("L", (3, 1))
    image.putdata([64, 128, 192])

    grayscale_image = convert_to_grayscale(image, contrast=2.0)
    dark_pixel = grayscale_image.getpixel((0, 0))
    mid_pixel = grayscale_image.getpixel((1, 0))
    light_pixel = grayscale_image.getpixel((2, 0))

    assert isinstance(dark_pixel, int) and dark_pixel < 64
    assert mid_pixel == 128
    assert isinstance(light_pixel, int) and light_pixel > 192


def test_convert_to_grayscale_does_not_modify_original():
    image = Image.new("RGB", (1, 1), color=(255, 0, 0))

    convert_to_grayscale(image)

    assert image.mode == "RGB"
    assert image.getpixel((0, 0)) == (255, 0, 0)


def test_negative_contrast_is_rejected():
    image = Image.new("L", (1, 1))

    with pytest.raises(ValueError, match="Contrast must be greater than or equal to 0"):
        convert_to_grayscale(image, contrast=-1.0)