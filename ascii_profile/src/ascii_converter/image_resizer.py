# ascii_profile/src/ascii_converter/image_loader.py

from PIL import Image


def resize_image(image: Image.Image, new_size: tuple) -> Image.Image:
    """
    Resize the given image to the specified new size.

    :param image: The original PIL Image object.
    :param new_size: A tuple (width, height) specifying the new size.
    :return: A new PIL Image object resized to the specified dimensions.
    """
    return image.resize(new_size, resample=Image.Resampling.LANCZOS)