# ascii_profile/src/ascii_converter/image_loader.py

from PIL import Image
from ascii_converter.grayscale import convert_to_grayscale

def load_image(image_path: str) -> Image.Image:
    img = Image.open(image_path)
    img = convert_to_grayscale(img, contrast=1.8)  # Convert the image to grayscale
    return img

