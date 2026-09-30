# ascii_profile/src/ascii_converter/generate.py

import os

from pathlib import Path
from ascii_converter.image_loader import load_image
from ascii_converter.image_resizer import resize_image
from ascii_converter.converter import image_to_ascii
from ascii_converter.layout import build_profile_svg
from ascii_converter.profile import Profile
from ascii_converter.github import GitHubStats
from ascii_converter.github import get_github_stats
from datetime import datetime, timezone


GITHUB_USERNAME = "yerdnarthc"
PORTRAIT_IMAGE_PATH = Path("C:\\Users\\Arth Andrey\\Pictures\\portrait_4.png")
OUTPUT_SVG_PATH = Path("profile.svg")


def generate_profile() -> None:

    # Load the image
    image = load_image(PORTRAIT_IMAGE_PATH)  

    # Desired dimensions
    width, height = 55, 38 

    # Resize the image
    image = resize_image(image, (width, height))  

    # Convert the image to ASCII
    ascii_art = image_to_ascii(image)

    # Create a profile object with your details
    profile = Profile(
        username=f"{GITHUB_USERNAME}@github",   # @github is optional, but it helps to clarify the platform
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

    token = os.environ["GITHUB_TOKEN"]

    # # Create the GithubStats object using the provided username and token
    # TEMP DEBUG: debug=True prints per-repo +A/-D lines so you can
    # verify the LOC totals. Set back to False (or remove) when done.
    github_stats = get_github_stats(
        GITHUB_USERNAME,
        token,
        datetime(2008, 1, 1, tzinfo=timezone.utc),  # Start date
        datetime.now(timezone.utc),  # End date
        debug=False,
    )

    # Build the SVG with the ASCII art and profile information
    svg = build_profile_svg(
        ascii_art, 
        profile,
        github_stats
    )

    # # Save the ASCII art to a text file
    # with open("ascii_art.txt", "w") as f:
    #     f.write(ascii_art)

    # print(ascii_art)  # Print the ASCII art to the console

    # Save the SVG to the output file
    OUTPUT_SVG_PATH.write_text(
        svg,
        encoding="utf-8"
    )
    
    print(f"Generated {OUTPUT_SVG_PATH}")