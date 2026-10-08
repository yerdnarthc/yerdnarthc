# ascii_profile/src/ascii_converter/profile_data.py

from datetime import date, datetime, timedelta, timezone

from .profile import Profile

GITHUB_USERNAME = "yerdnarthc"
BIRTH_DATE = date(2005, 9, 1)
# A fixed UTC+8 offset works on Windows and Linux without a timezone database.
PHILIPPINE_TIMEZONE = timezone(timedelta(hours=8), name="PHT")


def calculate_uptime(as_of: date | None = None) -> str:
    """Return calendar age since September 1, 2005, using the Philippine date."""
    if as_of is None:
        as_of = datetime.now(PHILIPPINE_TIMEZONE).date()
    if as_of < BIRTH_DATE:
        raise ValueError("Uptime date cannot be earlier than the birth date.")

    # The birthday is the first of the month, so every month starts a new
    # completed calendar month; the remaining days are counted from that day.
    total_months = (as_of.year - BIRTH_DATE.year) * 12 + as_of.month - BIRTH_DATE.month
    years, months = divmod(total_months, 12)
    days = as_of.day - BIRTH_DATE.day
    return ", ".join(
        f"{value} {unit}{'' if value == 1 else 's'}"
        for value, unit in ((years, "year"), (months, "month"), (days, "day"))
    )


def create_profile() -> Profile:
    """Return shared profile fields with uptime calculated on every call.

    GitHubStats stay separate (fetched live), so this only owns the
    username, OS, contacts, and the current calendar age.
    Edit them here once instead of in both main.py and update_profile.py.
    """
    return Profile(
        username=f"{GITHUB_USERNAME}@github",
        operating_system="Windows 11",
        uptime=calculate_uptime(),
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
