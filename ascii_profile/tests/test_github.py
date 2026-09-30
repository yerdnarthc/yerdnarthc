from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from ascii_converter.github import get_commit_count, get_contribution_stats, get_total_code_changes


def test_get_commit_count_all_time():
    responses = [
        {
            "data": {
                "user": {
                    "contributionsCollection": {
                        "contributionCalendar": {
                            "totalContributions": 100,
                        },
                        "totalCommitContributions": 100
                    }
                }
            }
        },
        {
            "data": {
                "user": {
                    "contributionsCollection": {
                        "contributionCalendar": {
                            "totalContributions": 200,
                        },
                        "totalCommitContributions": 200
                    }
                }
            }
        },
        {
            "data": {
                "user": {
                    "contributionsCollection": {
                        "contributionCalendar": {
                            "totalContributions": 0,
                        },
                        "totalCommitContributions": 0
                    }
                }
            }
        },
    ]

    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end = datetime(2026, 1, 1, tzinfo=timezone.utc)

    with patch(
        "ascii_converter.github._post_json",
        side_effect=responses,
    ):
        result = get_commit_count(
            "yerdnarthc",
            "fake-token",
            start,
            end,
        )

    assert result == 300


def test_get_contribution_stats_all_time():
    responses = [
        {
            "data": {
                "user": {
                    "contributionsCollection": {
                        "contributionCalendar": {
                            "totalContributions": 150,
                        },
                        "totalCommitContributions": 100,
                    }
                }
            }
        },
        {
            "data": {
                "user": {
                    "contributionsCollection": {
                            "contributionCalendar": {
                                "totalContributions": 250,
                            },
                        "totalCommitContributions": 200,
                    }
                }
            }
        },
            {
                "data": {
                    "user": {
                        "contributionsCollection": {
                            "contributionCalendar": {
                                "totalContributions": 0,
                            },
                            "totalCommitContributions": 0,
                        }
                    }
                }
            },
    ]

    start = datetime(
        2024,
        1,
        1,
        tzinfo=timezone.utc,
    )

    end = datetime(
        2026,
        1,
        1,
        tzinfo=timezone.utc,
    )

    with patch(
        "ascii_converter.github._post_json",
        side_effect=responses,
    ):
        contributions, commits = get_contribution_stats(
            "yerdnarthc",
            "fake-token",
            start,
            end,
        )

    assert contributions == 400
    assert commits == 300


def test_get_total_code_changes():
    repositories_response = [
        {"name": "repo-a"},
        {"name": "repo-b"},
    ]

    contributor_response = [
        {
            "author": {
                "login": "yerdnarthc"
            },
            "weeks": [
                {"a": 100, "d": 20, "c": 5},
                {"a": 50, "d": 10, "c": 2},
            ],
        }
    ]

    responses = []
    for _ in repositories_response:
        response = MagicMock()
        response.status = 200
        response.__enter__.return_value = response
        responses.append(response)

    with (
        patch(
            "ascii_converter.github._get_json",
            side_effect=[repositories_response, []],
        ),
        patch(
            "ascii_converter.github.urlopen",
            side_effect=responses,
        ),
        patch(
            "ascii_converter.github.json.load",
            side_effect=[contributor_response, contributor_response],
        ),
    ):
        added, removed = get_total_code_changes(
            "yerdnarthc",
            {
                "Accept": "application/vnd.github+json",
            },
        )

    assert added == 300
    assert removed == 60