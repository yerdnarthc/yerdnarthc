# ascii_profile/src/ascii_converter/generate.py

import os

from pathlib import Path
from ascii_converter.image_loader import load_image
from ascii_converter.image_resizer import resize_image
from ascii_converter.converter import image_to_ascii
from ascii_converter.layout import build_profile_svg
from ascii_converter.profile_data import GITHUB_USERNAME, create_profile
from ascii_converter.github import get_github_stats
from datetime import datetime, timezone

# Change this to your actual portrait image path.
PORTRAIT_IMAGE_PATH = Path("C:\\Users\\Arth Andrey\\Pictures\\portrait_4.png")

# File-relative so it works no matter which cwd you run from.
OUTPUT_SVG_PATH = Path(__file__).resolve().parent.parent.parent / "profile.svg"


def generate_profile() -> None:

    # Load the image
    image = load_image(PORTRAIT_IMAGE_PATH)

    # Desired dimensions
    width, height = 47, 32

    # Resize the image
    image = resize_image(image, (width, height))

    # Convert the image to ASCII
    ascii_art = image_to_ascii(image)

    # Static profile fields (single source of truth in profile_data.py)
    profile = create_profile()

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

    # Save the SVG to the output file
    OUTPUT_SVG_PATH.write_text(
        svg,
        encoding="utf-8"
    )
    
    print(f"Generated {OUTPUT_SVG_PATH}")