# ascii_profile/tests/test_resize.py

import pytest
from ascii_converter.image_resizer import resize_image
from ascii_converter.image_loader import load_image
from PIL import Image


@pytest.mark.parametrize("new_size", [(2, 2), (8, 4), (80, 24)])
def test_resize_image_to_custom_size(new_size):
    image = Image.new("L", (4, 4))
    image.putdata([0, 64, 128, 192] * 4)

    resized_image = resize_image(image, new_size)

    assert resized_image.size == new_size
    assert resized_image.mode == image.mode


def test_resize_image_does_not_modify_original():
    image = Image.new("L", (4, 4), color=128)

    resized_image = resize_image(image, (2, 2))

    assert image.size == (4, 4)
    assert resized_image.size == (2, 2)


def test_resize_image_with_invalid_size():
    image = Image.new("L", (4, 4), color=128)

    with pytest.raises(ValueError):
        resize_image(image, (-1, 2))

    with pytest.raises(ValueError):
        resize_image(image, (2, -1))

    with pytest.raises(ValueError):
        resize_image(image, (0, 0))


def test_resize_image_with_non_integer_size():
    image = Image.new("L", (4, 4), color=128)

    with pytest.raises(TypeError):
        resize_image(image, (2.5, 2))

    with pytest.raises(TypeError):
        resize_image(image, (2, "3"))


def test_resize_image_with_large_size():
    image = Image.new("L", (4, 4), color=128)

    new_size = (1000, 1000)
    resized_image = resize_image(image, new_size)

    assert resized_image.size == new_size


def test_resize_image_after_loading(tmp_path):
    source_path = tmp_path / "source.png"
    source_image = Image.new("RGB", (10, 12), color=(255, 0, 0))
    source_image.save(source_path)

    image = load_image(source_path)
    new_size = (100, 120)
    resized_image = resize_image(image, new_size)

    assert resized_image.size == new_size
    assert image.size == (10, 12)