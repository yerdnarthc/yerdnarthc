# ascii_profile/tests/test_loader.py

import pytest
from PIL import Image

from ascii_converter.grayscale import convert_to_grayscale
from ascii_converter.image_loader import load_image


def test_load_image_grayscale(tmp_path):
    # Create a simple 2x2 image for testing
    test_image = Image.new("L", (2, 2))
    test_image.putdata([0, 255, 255, 0])  # Black and white pixels

    # Save the test image to a temporary file
    temp_image_path = tmp_path / "test_image.png"
    test_image.save(temp_image_path)

    # Load the image using the load_image function
    loaded_image = load_image(temp_image_path)

    # Check if the loaded image has the same size and pixel values as the original
    assert loaded_image.size == test_image.size
    expected_image = convert_to_grayscale(test_image, contrast=1.8)
    assert list(loaded_image.get_flattened_data()) == list(expected_image.get_flattened_data())


def test_load_image_invalid_path():
    # Test loading an image from an invalid path
    invalid_image_path = "non_existent_image.png"
    try:
        load_image(invalid_image_path)
    except FileNotFoundError as e:
        assert str(e) == f"[Errno 2] No such file or directory: '{invalid_image_path}'"


def test_load_image_non_image_file(tmp_path):
    # Test loading a non-image file
    non_image_file_path = tmp_path / "test_file.txt"
    with open(non_image_file_path, "w") as f:
        f.write("This is not an image.")

    with pytest.raises(OSError, match="cannot identify image file"):
        load_image(non_image_file_path)


def test_load_image_color_image(tmp_path):
    # Create a simple 2x2 color image for testing
    test_color_image = Image.new("RGB", (2, 2))
    test_color_image.putdata([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)])  # Red, Green, Blue, Yellow

    # Save the test color image to a temporary file
    temp_color_image_path = tmp_path / "test_color_image.png"
    test_color_image.save(temp_color_image_path)

    # Load the image using the load_image function
    loaded_image = load_image(temp_color_image_path)

    # Check if the loaded image is in grayscale mode
    assert loaded_image.mode == "L"

    # Check if the loaded image has the same size as the original
    assert loaded_image.size == test_color_image.size

    expected_image = convert_to_grayscale(test_color_image, contrast=1.8)
    assert list(loaded_image.get_flattened_data()) == list(expected_image.get_flattened_data())


def test_load_image_large_image(tmp_path):
    # Create a large image (e.g., 1000x1000 pixels) for testing
    width, height = 100, 100
    test_large_image = Image.new("L", (width, height))
    test_large_image.putdata([i % 256 for i in range(width * height)])  # Gradient pixel values

    # Save the test large image to a temporary file
    temp_large_image_path = tmp_path / "test_large_image.png"
    test_large_image.save(temp_large_image_path)

    # Load the image using the load_image function
    loaded_image = load_image(temp_large_image_path)

    # Check if the loaded image has the same size and pixel values as the original
    assert loaded_image.size == test_large_image.size
    expected_image = convert_to_grayscale(test_large_image, contrast=1.8)
    assert list(loaded_image.get_flattened_data()) == list(expected_image.get_flattened_data())


def test_load_and_save_image(tmp_path):
    source_path = tmp_path / "source.png"
    saved_path = tmp_path / "saved.png"
    source_image = Image.new("RGB", (2, 2), color=(255, 0, 0))
    source_image.save(source_path)

    loaded_image = load_image(source_path)
    loaded_image.save(saved_path)

    reloaded_image = Image.open(saved_path)
    assert reloaded_image.mode == loaded_image.mode
    assert reloaded_image.size == loaded_image.size
    assert list(reloaded_image.get_flattened_data()) == list(loaded_image.get_flattened_data())