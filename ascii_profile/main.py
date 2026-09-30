# ascii_profile/main.py

from PIL import Image
from ascii_converter.image_loader import load_image
from ascii_converter.image_resizer import resize_image
from ascii_converter.converter import image_to_ascii
from ascii_converter.svg import ascii_to_svg
from ascii_converter.layout import build_profile_svg
from ascii_converter.profile import Profile

INPUT_IMAGE_PATH = r"C:\Users\Arth Andrey\Pictures\portrait_4.png"
OUTPUT_SVG_PATH = r"ascii_art_preview.svg"

# Load the image
image = load_image(INPUT_IMAGE_PATH)  

# Desired dimensions
width, height = 55, 38 

# Resize the image
image = resize_image(image, (width, height))  

# Convert the image to ASCII
ascii_art = image_to_ascii(image)

# Create a profile object with your details
profile = Profile(
    username="yerdnarthc@github",
    operating_system="Windows 11",
    uptime="21 years, 0 months, 29 days",
    host="Lenovo IdeaPad Slim 5 16IMH9",
    kernel="Windows NT",
    ide="Visual Studio, VS Code, IntelliJ IDEA",

    projects=[
        "BantAI", 
        "N-Queens Visualizer",
        "VWSIM",
        "DeskDuck",
    ],
    programming_languages=[
        "C", 
        "C++",
        "C#",
        "Python", 
        "JavaScript",
        "Java",
    ],
    other_languages=[
        "HTML", 
        "CSS",
        "SQL",
        "Bash",
        "PowerShell",
        "JSON",
    ],
    real_languages=[
        "English", 
        "Filipino",
        "Cebuano",
    ],
    software_hobbies=[
        "Music Production", 
        "VFX",
        "Video Editing",
    ],
    hardware_hobbies=[
        "Tinkering", 
        "Benchmarking",
        "Audio Gear"
    ],
    
    email_personal="arthandrey16@gmail.com",
    email_institutional="arthandrey.endrina@cit.edu",
    linkedin="Arth Andrey Endrina",
    discord="iamyerdna",
)

# Build the SVG with the ASCII art and profile information
svg = build_profile_svg(ascii_art, profile)

# # Save the ASCII art to a text file
# with open("ascii_art.txt", "w") as f:
#     f.write(ascii_art)

# print(ascii_art)  # Print the ASCII art to the console

# Save the SVG to a file
with open(OUTPUT_SVG_PATH, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Generated {OUTPUT_SVG_PATH}")