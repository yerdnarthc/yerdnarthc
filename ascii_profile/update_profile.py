# ascii_profile/update_profile.py
#
# Automated updater for GitHub Actions. Reads the already-committed
# profile.svg, reuses its embedded ASCII portrait, fetches fresh GitHub
# stats, and rewrites profile.svg. Never touches the portrait image,
# so no Pillow / converter imports here by design.

import os
from datetime import datetime, timezone
from pathlib import Path

from ascii_converter.github import get_github_stats
from ascii_converter.layout import (
    build_profile_svg_from_portrait,
    extract_portrait_svg,
)
from ascii_converter.profile_data import GITHUB_USERNAME, create_profile

PROFILE_SVG_PATH = Path(__file__).resolve().parent / "profile.svg"


def main() -> None:
    token = os.environ["GITHUB_TOKEN"]

    # --------------------------------------------------------
    # Read existing SVG
    # --------------------------------------------------------
    existing_svg = PROFILE_SVG_PATH.read_text(encoding="utf-8")

    # --------------------------------------------------------
    # Extract the already-embedded ASCII portrait
    # --------------------------------------------------------
    portrait_svg = extract_portrait_svg(existing_svg)

    # --------------------------------------------------------
    # Get current GitHub statistics
    # --------------------------------------------------------
    github_stats = get_github_stats(
        GITHUB_USERNAME,
        token,
        datetime(2008, 1, 1, tzinfo=timezone.utc),
        datetime.now(timezone.utc),
    )

    # --------------------------------------------------------
    # Rebuild profile data (static fields from profile_data.py)
    # --------------------------------------------------------
    profile = create_profile()

    # --------------------------------------------------------
    # Rebuild SVG using existing portrait
    # --------------------------------------------------------
    svg = build_profile_svg_from_portrait(
        portrait_svg,
        profile,
        github_stats,
    )

    PROFILE_SVG_PATH.write_text(svg, encoding="utf-8")

    print("Updated profile.svg")


if __name__ == "__main__":
    main()
