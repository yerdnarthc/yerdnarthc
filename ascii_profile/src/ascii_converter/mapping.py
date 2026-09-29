# ascii_converter/mapping.py

from PIL import Image

CHARSET = "@%#A$&R?TBH|][()wgarh!:;i=^~+<>*'-_,. "    # 38 characters in length

# ================== ASCII MAPPING FUNCTIONS ==================

def pixel_to_char(value) -> str:
    """
    Convert a pixel value (0-255) to a character from the CHARSET.
    """

    # Map the pixel value to an index in the CHARSET
    index = value_to_charset_index(value)
    return CHARSET[index]


def value_to_charset_index(value):
    """
    Convert a pixel value (0-255) to an index in the CHARSET.
    """
    if not (0 <= value <= 255):
        raise ValueError("Pixel value must be between 0 and 255.")

    inverted_value = 255 - value  # Invert the pixel value for mapping
    return int((inverted_value / 255) * (len(CHARSET) - 1))


# ================== TEMPORARY FUNCTIONS FOR TESTING PURPOSES ==================

def make_checkerboard(width, height):
    """
    Create a checkerboard pattern of pixel values.
    """
    image = Image.new("L", (width, height))

    pixels = []

    for y in range(height):
        for x in range(width):
            pixels.append(
                0 if (x + y) % 2 == 0 else 255  # Black and white checkerboard pattern
            )

    image.putdata(pixels)
    return image


def make_three_tone_checkerboard(width, height):
    """
    Create a checkerboard pattern with three tones of pixel values.
    """
    image = Image.new("L", (width, height))

    pixels = []

    end = 0
    index_to_pixel = 0

    for y in range(height):
        for x in range(width):
            index_to_pixel = end + x
            if index_to_pixel % 3 == 0:
                pixels.append(0)  # Black
            elif index_to_pixel % 3 == 1:
                pixels.append(128)  # Mid-gray
            else:
                pixels.append(255)  # White

        end = index_to_pixel + 1

    image.putdata(pixels)
    return image


def checkerboard_to_ascii(image):
    """
    Convert a checkerboard image to ASCII art.
    """
    ascii_art = []
    for y in range(image.height):
        ascii_art_row = ""
        for x in range(image.width):
            pixel_value = image.getpixel((x, y))
            ascii_art_row += pixel_to_char(pixel_value)
        ascii_art.append(ascii_art_row)
    return ascii_art


def three_tone_checkerboard_to_ascii(image):
    """
    Convert a three-tone checkerboard image to ASCII art.
    """
    ascii_art = []
    for y in range(image.height):
        ascii_art_row = ""
        for x in range(image.width):
            pixel_value = image.getpixel((x, y))
            ascii_art_row += pixel_to_char(pixel_value)
        ascii_art.append(ascii_art_row)
    return ascii_art

