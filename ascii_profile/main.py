# ascii_profile/main.py

from PIL import Image
from ascii_converter.image_loader import load_image
from ascii_converter.image_resizer import resize_image
from ascii_converter.converter import image_to_ascii
from ascii_converter.svg import ascii_to_svg
from ascii_converter.layout import build_profile_svg

INPUT_IMAGE_PATH = r"C:\Users\Arth Andrey\Pictures\portrait_4.png"
OUTPUT_SVG_PATH = r"ascii_art_preview.svg"


image = load_image(INPUT_IMAGE_PATH)  # Load the image

width, height = 55, 38 # Desired dimensions

image = resize_image(image, (width, height))  # Resize the image

ascii_art = image_to_ascii(image)  # Convert the image to ASCII

svg = build_profile_svg(ascii_art)  # Build the SVG with the ASCII art

# # Save the ASCII art to a text file
# with open("ascii_art.txt", "w") as f:
#     f.write(ascii_art)

# print(ascii_art)  # Print the ASCII art to the console

# Save the SVG to a file
with open(OUTPUT_SVG_PATH, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Generated {OUTPUT_SVG_PATH}")