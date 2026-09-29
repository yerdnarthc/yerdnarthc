# ascii_profile/src/ascii_converter/image_loader.py

from PIL import Image

def load_image(image_path: str) -> Image.Image:
    img = Image.open(image_path)
    img = img.convert("L")  # Convert to grayscale
    return img

