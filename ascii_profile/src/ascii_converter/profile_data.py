# ascii_profile/src/ascii_converter/profile_data.py

from .profile import Profile

GITHUB_USERNAME = "yerdnarthc"


def create_profile() -> Profile:
    """Return the static profile fields shared by local + automated runs.

    GitHubStats stay separate (fetched live), so this only owns the
    parts that rarely change: username, OS, contacts, etc.
    Edit them here once instead of in both main.py and update_profile.py.
    """
    return Profile(
        username=f"{GITHUB_USERNAME}@github",
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
            "Audio Gear",
        ],
        email_personal="arthandrey16@gmail.com",
        email_institutional="arthandrey.endrina@cit.edu",
        linkedin="Arth Andrey Endrina",
        discord="iamyerdna",
    )
