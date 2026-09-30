# ascii_profile/main.py

from PIL import Image
from ascii_converter.image_loader import load_image
from ascii_converter.image_resizer import resize_image
from ascii_converter.converter import image_to_ascii
from ascii_converter.svg import ascii_to_svg


image = load_image("C:\\Users\\Arth Andrey\\Pictures\\portrait_4.png")  # Load the image
width, height = 60, 35 # Desired dimensions
image = resize_image(image, (width, height))  # Resize the image
ascii_art = image_to_ascii(image)  # Convert the image to ASCII

svg = ascii_to_svg(
    ascii_art, 
    font_size=15, 
    font_family="Consolas", 
    char_width=7.5,
)

# # Save the ASCII art to a text file
# with open("ascii_art.txt", "w") as f:
#     f.write(ascii_art)

# print(ascii_art)  # Print the ASCII art to the console

with open("ascii_art_preview.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("Generated ascii_art_preview.svg")