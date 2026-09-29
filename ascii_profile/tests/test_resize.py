# ascii_profile/tests/test_resize.py

import pytest, os
from ascii_converter.image_resizer import resize_image
from ascii_converter.image_loader import load_image     # temporary only
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


def test_resize_image_after_loading():
    # Temporarily use ascii_converter.image_loader.load_image to load an image for testing
    image = load_image("C:\\Users\\Arth Andrey\\Pictures\\portrait.jpg")

    # Temporarily save the loaded image for previewing purposes
    image.save("before_resize_preview.jpg")

    new_size = (100, 120)
    resized_image = resize_image(image, new_size)

    # Temporarily save the resized image for previewing purposes
    resized_image.save("after_resize_preview.jpg")

    assert resized_image.size == new_size

    assert image.get_flattened_data() != resized_image.get_flattened_data()

    os.remove("before_resize_preview.jpg")
    os.remove("after_resize_preview.jpg")