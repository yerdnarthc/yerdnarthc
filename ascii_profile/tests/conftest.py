# ascii_profile/tests/conftest.py

import pytest
from ascii_converter.profile import Profile, GitHubStats


@pytest.fixture
def test_profile():
    return Profile(
        username="test@github",
        operating_system="Test OS",
        uptime="0 days",
        host="Test Host",
        kernel="Test Kernel",
        ide="Test IDE",
        projects=["Project A", "Project B"],
        programming_languages=["Python", "C++"],
        other_languages=["HTML", "CSS"],
        real_languages=["English"],
        software_hobbies=["Testing"],
        hardware_hobbies=["Tinkering"],
        email_personal="personal@example.com",
        email_institutional="school@example.edu",
        linkedin="Test User",
        discord="test",
    )

@pytest.fixture
def test_github_stats():
    return GitHubStats(
        repositories=10,
        stars=50,
        commits=100,
        followers=200
    )