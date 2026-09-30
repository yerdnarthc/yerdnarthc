from datetime import datetime, timezone
from unittest.mock import patch

from ascii_converter.github import get_commit_count


def test_get_commit_count_all_time():
    responses = [
        {
            "data": {
                "user": {
                    "contributionsCollection": {
                        "totalCommitContributions": 100
                    }
                }
            }
        },
        {
            "data": {
                "user": {
                    "contributionsCollection": {
                        "totalCommitContributions": 200
                    }
                }
            }
        },
        {
            "data": {
                "user": {
                    "contributionsCollection": {
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