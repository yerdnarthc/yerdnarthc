# ascii_profile/src/ascii_converter/mapping.py

from PIL import Image
from ascii_converter.mapping import pixel_to_char


def image_to_ascii(image: Image.Image) -> str:
    """
    Convert a PIL Image to an ASCII string representation.
    :param image: A PIL Image object.
    :return: A string containing the ASCII representation of the image.
    """
    # Ensure the image is in grayscale mode
    if image.mode != "L":
        raise ValueError("Image must be in grayscale mode (L).")

    width, height = image.size
    rows = []

    for y in range(height):
        row = []

        for x in range(width):
            pixel_value = image.getpixel((x, y))
            ascii_char = pixel_to_char(pixel_value)
            row.append(ascii_char)

        rows.append("".join(row))

    return "\n".join(rows) + "\n"   # Add a newline at the end for better formatting
            