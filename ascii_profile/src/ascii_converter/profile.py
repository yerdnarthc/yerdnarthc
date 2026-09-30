# ascii_profile/src/ascii_converter/profile.py

from dataclasses import dataclass

@dataclass
class Profile:
    username: str
    operating_system: str
    uptime: str
    host: str
    kernel: str
    ide: str
    projects: list[str]

    programming_languages: list[str]
    other_languages: list[str]
    real_languages: list[str]

    software_hobbies: list[str]
    hardware_hobbies: list[str]

    email_personal: str
    email_institutional: str
    linkedin: str
    discord: str