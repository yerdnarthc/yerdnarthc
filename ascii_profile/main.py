# ascii_profile/main.py

from PIL import Image
from ascii_converter.image_loader import load_image
from ascii_converter.image_resizer import resize_image
from ascii_converter.converter import image_to_ascii



image = load_image("C:\\Users\\Arth Andrey\\Pictures\\portrait.jpg")  # Load the image
width, height = 100, 50 # Desired dimensions
image = resize_image(image, (width, height))  # Resize the image
ascii_art = image_to_ascii(image)  # Convert the image to ASCII

# # Save the ASCII art to a text file
# with open("ascii_art.txt", "w") as f:
#     f.write(ascii_art)

print(ascii_art)  # Print the ASCII art to the console