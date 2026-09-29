# ascii_profile/tests/test_loader.py

from PIL import Image
from ascii_converter.image_loader import load_image
import os


def test_load_image_grayscale():
    # Create a simple 2x2 image for testing
    test_image = Image.new("L", (2, 2))
    test_image.putdata([0, 255, 255, 0])  # Black and white pixels

    # Save the test image to a temporary file
    temp_image_path = "temp_test_image.png"
    test_image.save(temp_image_path)

    # Load the image using the load_image function
    loaded_image = load_image(temp_image_path)

    # Check if the loaded image has the same size and pixel values as the original
    assert loaded_image.size == test_image.size
    assert list(loaded_image.get_flattened_data()) == list(test_image.get_flattened_data())

    # Clean up the temporary file
    os.remove(temp_image_path)


def test_load_image_invalid_path():
    # Test loading an image from an invalid path
    invalid_image_path = "non_existent_image.png"
    try:
        load_image(invalid_image_path)
    except FileNotFoundError as e:
        assert str(e) == f"[Errno 2] No such file or directory: '{invalid_image_path}'"


def test_load_image_non_image_file():
    # Test loading a non-image file
    non_image_file_path = "temp_test_file.txt"
    with open(non_image_file_path, "w") as f:
        f.write("This is not an image.")

    try:
        load_image(non_image_file_path)
    except OSError as e:
        assert str(e).startswith("cannot identify image file")

    finally:
        # Clean up the temporary file
        os.remove(non_image_file_path)


def test_load_image_color_image():
    # Create a simple 2x2 color image for testing
    test_color_image = Image.new("RGB", (2, 2))
    test_color_image.putdata([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)])  # Red, Green, Blue, Yellow

    # Save the test color image to a temporary file
    temp_color_image_path = "temp_test_color_image.png"
    test_color_image.save(temp_color_image_path)

    # Load the image using the load_image function
    loaded_image = load_image(temp_color_image_path)

    # Check if the loaded image is in grayscale mode
    assert loaded_image.mode == "L"

    # Check if the loaded image has the same size as the original
    assert loaded_image.size == test_color_image.size

    # Check if the loaded image has the same pixel values as the original (in grayscale)
    assert list(loaded_image.get_flattened_data()) == list(test_color_image.convert("L").get_flattened_data())

    # Clean up the temporary file
    os.remove(temp_color_image_path)


def test_load_image_large_image():
    # Create a large image (e.g., 1000x1000 pixels) for testing
    width, height = 1000, 1000
    test_large_image = Image.new("L", (width, height))
    test_large_image.putdata([i % 256 for i in range(width * height)])  # Gradient pixel values

    # Save the test large image to a temporary file
    temp_large_image_path = "temp_test_large_image.png"
    test_large_image.save(temp_large_image_path)

    # Load the image using the load_image function
    loaded_image = load_image(temp_large_image_path)

    # Check if the loaded image has the same size and pixel values as the original
    assert loaded_image.size == test_large_image.size
    assert list(loaded_image.get_flattened_data()) == list(test_large_image.get_flattened_data())

    # # Clean up the temporary file
    os.remove(temp_large_image_path)


def test_load_existing_image():
    # Test loading an existing image file
    existing_image_path = "C:\\Users\\Arth Andrey\\Pictures\\portrait.jpg"

    # Load the image using the load_image function
    loaded_image = load_image(existing_image_path)

    # Check if the image is loaded and is in grayscale mode
    assert loaded_image is not None and loaded_image.mode == "L"


def test_load_and_save_temp_existing_image():
    # Test loading an existing image file and saving it to a temporary file
    existing_image_path = "C:\\Users\\Arth Andrey\\Pictures\\portrait.jpg"
    temp_image_path = "temp_test_existing_image.png"

    # Load the image using the load_image function
    loaded_image = load_image(existing_image_path)

    # Save the loaded image to a temporary file
    loaded_image.save(temp_image_path)

    # Load the saved image back and check if it matches the original loaded image
    reloaded_image = load_image(temp_image_path)
    assert list(reloaded_image.get_flattened_data()) == list(loaded_image.get_flattened_data())

    # # Clean up the temporary file
    os.remove(temp_image_path)