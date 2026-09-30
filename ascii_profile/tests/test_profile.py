import xml.etree.ElementTree as ET

from ascii_converter.profile import Profile
from ascii_converter.layout import build_profile_svg


def svg_text_nodes(svg: str) -> list[str]:
    root = ET.fromstring(svg)
    return [
        "".join(element.itertext())
        for element in root.iter()
        if element.tag.endswith("text")
    ]


def test_profile_stores_basic_information():
    profile = Profile(
        username="arth@github",
        operating_system="Windows 11",
        uptime="21 years, 0 months, 29 days",
        host="Test PC",
        kernel="Windows NT",
        ide="VS Code",
        projects=[],
        programming_languages=[],
        other_languages=[],
        real_languages=[],
        software_hobbies=[],
        hardware_hobbies=[],
        email_personal="test@example.com",
        email_institutional="school@example.edu",
        linkedin="Test User",
        discord="test_discord_user",
    )

    assert profile.username == "arth@github"
    assert profile.host == "Test PC"


def test_profile_information_appears_in_svg(test_profile, test_github_stats):
    svg = build_profile_svg("@", test_profile, test_github_stats)

    assert test_profile.username in svg
    assert test_profile.operating_system in svg
    assert test_profile.host in svg


def test_profile_with_empty_fields(test_github_stats):
    profile = Profile(
        username="",
        operating_system="",
        uptime="",
        host="",
        kernel="",
        ide="",
        projects=[],
        programming_languages=[],
        other_languages=[],
        real_languages=[],
        software_hobbies=[],
        hardware_hobbies=[],
        email_personal="",
        email_institutional="",
        linkedin="",
        discord="",
    )

    svg = build_profile_svg("@", profile, test_github_stats)

    # Ensure that the SVG is generated without errors and contains the ASCII art
    assert svg.startswith("<svg")
    assert "@" in svg


def test_profile_information_is_present_and_same_in_svg(test_github_stats):
    profile = Profile(
        username="arth@github",
        operating_system="Windows 11",
        uptime="21 years, 0 months, 29 days",
        host="Test PC",
        kernel="Windows NT",
        ide="VS Code",
        projects=[],
        programming_languages=[],
        other_languages=[],
        real_languages=[],
        software_hobbies=[],
        hardware_hobbies=[],
        email_personal="test@example.com",
        email_institutional="test@cit.edu",
        linkedin="Test User",
        discord="test_discord_user",
    )

    svg = build_profile_svg("@", profile, test_github_stats)

    # Check that all profile information is present in the SVG
    assert profile.username in svg
    assert profile.operating_system in svg
    assert profile.uptime in svg
    assert profile.host in svg
    assert profile.kernel in svg
    assert profile.ide in svg
    assert profile.projects == []  # Projects list is empty
    assert profile.programming_languages == []  # Programming languages list is empty
    assert profile.other_languages == []  # Other languages list is empty
    assert profile.real_languages == []  # Real languages list is empty
    assert profile.software_hobbies == []  # Software hobbies list is empty
    assert profile.hardware_hobbies == []  # Hardware hobbies list is empty
    assert profile.email_personal in svg
    assert profile.email_institutional in svg
    assert profile.linkedin in svg
    assert profile.discord in svg

    # Compare exact rendered text nodes, avoiding substring-count collisions.
    rendered_text = svg_text_nodes(svg)
    expected_text = [
        profile.username,
        profile.operating_system,
        profile.uptime,
        profile.host,
        profile.kernel,
        profile.ide,
        profile.email_personal,
        profile.email_institutional,
        profile.linkedin,
        profile.discord,
    ]

    for items in (
        profile.projects,
        profile.programming_languages,
        profile.other_languages,
        profile.real_languages,
        profile.software_hobbies,
        profile.hardware_hobbies,
    ):
        if items:
            expected_text.append(", ".join(items))

    for value in expected_text:
        assert value in rendered_text

    assert "10 {Contributed: TBA}" in rendered_text
    assert "50" in rendered_text
    assert "100" in rendered_text
    assert "200" in rendered_text