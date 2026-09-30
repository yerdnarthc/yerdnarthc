# ascii_profile/src/ascii_converter/github.py

import json
import time
import warnings

from typing import Any
from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .profile import GitHubStats

"""
Note:
GitHub may return zero additions/deletions for repositories
with 10,000 or more commits.
"""

GITHUB_API_VERSION = "2026-03-10"
GITHUB_API = "https://api.github.com"
GITHUB_GRAPHQL_API = "https://api.github.com/graphql"


def _get_json(
    url: str, 
    headers: dict[str, str], 
    params: Mapping[str, str | int] | None = None
) -> Any:
    if params:
        url = f"{url}?{urlencode(params)}"

    request = Request(url, headers=headers)
    with urlopen(request, timeout=10) as response:
        if response.status >= 400:
            raise RuntimeError(f"GitHub API request failed with status {response.status}")
        return json.load(response)


def _post_json(
    url: str,
    headers: dict[str, str],
    payload: dict,
) -> Any:
    data = json.dumps(payload).encode("utf-8")

    request = Request(
        url,
        data=data,
        headers={
            **headers,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urlopen(request, timeout=10) as response:
        if response.status >= 400:
            raise RuntimeError(
                f"GitHub API request failed with status {response.status}"
            )

        return json.load(response)
    

def get_github_stats(
    username: str,
    token: str,
    start: datetime | None = None,
    end: datetime | None = None,
    debug: bool = False,
) -> GitHubStats:

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
    }

    user = _get_json(
        f"{GITHUB_API}/users/{username}",
        headers=headers,
    )

    repositories = user["public_repos"]
    followers = user["followers"]

    stars = get_total_stars(
        username,
        headers,
    )

    contributions, commits = get_contribution_stats(
        username,
        token,
        start,
        end,
    )

    lines_added, lines_removed = get_total_code_changes(
        username,
        headers,
        debug=debug,
    )

    lines_of_codes = lines_added + lines_removed

    return GitHubStats(
        repositories=repositories,
        commits=commits,
        contributions=contributions,
        stars=stars,
        followers=followers,
        lines_of_code=lines_of_codes,
        lines_of_code_additions=lines_added,
        lines_of_code_deletions=lines_removed,
    )


def get_total_stars(
    username: str,
    headers: dict[str, str],
) -> int:
    total = 0
    page = 1

    while True:
        repositories = _get_json(
            f"{GITHUB_API}/users/{username}/repos",
            headers=headers,
            params={
                "type": "owner",
                "per_page": 100,
                "page": page,
            },
        )

        if not repositories:
            break

        for repo in repositories:
            # # Temp debugging print statement to check the repository data
            # print(
            #     repo["full_name"],
            #     repo["stargazers_count"],
            # )

            total += repo["stargazers_count"]

        if len(repositories) < 100:
            break

        page += 1

    return total


def get_contribution_stats(
    username: str,
    token: str,
    start: datetime | None = None,
    end: datetime | None = None,
) -> tuple[int, int]:
    """
    Return all-time (or specified-range) contributions and commits.

    Returns:
        tuple[int, int]: (total_contributions, total_commits)
    """

    query = """
    query(
        $username: String!,
        $from: DateTime!,
        $to: DateTime!
    ) {
        user(login: $username) {
            contributionsCollection(
                from: $from,
                to: $to
            ) {
                contributionCalendar {
                    totalContributions
                }
                totalCommitContributions
            }
        }
    }
    """

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
    }

    if start is None:
        start = datetime(
            2008,
            1,
            1,
            tzinfo=timezone.utc,
        )

    if end is None:
        end = datetime.now(timezone.utc)

    total_contributions = 0
    total_commits = 0

    while start < end:
        next_end = min(
            start + timedelta(days=365),
            end,
        )

        payload = {
            "query": query,
            "variables": {
                "username": username,
                "from": start.isoformat(),
                "to": next_end.isoformat(),
            },
        }

        result = _post_json(
            GITHUB_GRAPHQL_API,
            headers=headers,
            payload=payload,
        )

        if "errors" in result:
            raise RuntimeError(
                f"GitHub GraphQL error: {result['errors']}"
            )

        try:
            collection = result["data"]["user"][
                "contributionsCollection"
            ]

            total_contributions += collection[
                "contributionCalendar"
            ]["totalContributions"]

            total_commits += collection[
                "totalCommitContributions"
            ]

        except (KeyError, TypeError):
            raise RuntimeError(
                f"Unexpected GitHub response: {result}"
            )

        start = next_end

    return total_contributions, total_commits


def get_commit_count(
    username: str,
    token: str,
    start: datetime | None = None,
    end: datetime | None = None,
) -> int:
    _, commits = get_contribution_stats(
        username,
        token,
        start,
        end,
    )

    return commits


def get_total_code_changes(
    username: str,
    headers: dict[str, str],
    debug: bool = False,
) -> tuple[int, int]:
    """
    Return total lines changed by the user across all owned public repositories.

    Args:
        debug: TEMPORARY — print per-repo additions/deletions so you can
            sanity-check the totals. Leave False in tests to keep output clean.

    Returns:
        tuple[int, int]: (lines_added, lines_removed)
    """

    total_added = 0
    total_removed = 0

    page = 1

    while True:
        repositories = _get_json(
            f"{GITHUB_API}/users/{username}/repos",
            headers=headers,
            params={
                "type": "owner",
                "per_page": 100,
                "page": page,
            },
        )

        if not repositories:
            break

        for repo in repositories:
            repo_name = repo["name"]

            stats_url = (
                f"{GITHUB_API}/repos/"
                f"{username}/{repo_name}/stats/contributors"
            )

            stats: list[dict] = []

            for attempt in range(6):
                request = Request(
                    stats_url,
                    headers=headers,
                )

                with urlopen(request, timeout=10) as response:
                    if response.status == 202:
                        # GitHub computes /stats on demand and replies
                        # 202 Accepted while it's working. This is normal
                        # for new, large, or rarely-viewed repos — it is
                        # not an error, just "try again shortly".
                        if attempt == 5:
                            # Fail soft: skip this repo so one slow repo
                            # (e.g. rag-messenger-backend) can't abort
                            # the whole profile pipeline.
                            warnings.warn(
                                f"GitHub statistics not ready for "
                                f"{username}/{repo_name}, skipping."
                            )
                            stats = []
                            break

                        time.sleep(2)
                        continue

                    if response.status == 204:
                        stats = []
                    elif response.status >= 400:
                        raise RuntimeError(
                            "GitHub API request failed with "
                            f"status {response.status}"
                        )
                    else:
                        stats = json.load(response)

                    break

            for contributor in stats:
                author = contributor.get("author")

                if (
                    author is None
                    or author.get("login", "").lower()
                    != username.lower()
                ):
                    continue

                # TEMP DEBUG: per-repo counters so you can see which
                # repo contributes how much to the grand total.
                repo_added = 0
                repo_removed = 0
                for week in contributor.get("weeks", []):
                    repo_added += week.get("a", 0)
                    repo_removed += week.get("d", 0)

                total_added += repo_added
                total_removed += repo_removed

                if debug:
                    print(
                        f"{repo_name:40} "
                        f"+{repo_added:>10,} "
                        f"-{repo_removed:>10,} "
                        f"| running total "
                        f"+{total_added:>10,} "
                        f"-{total_removed:>10,}"
                    )

                break
            else:
                # No matching contributor entry (e.g. empty repo or
                # stats=[] after 202-skip / 204-empty).
                if debug:
                    print(f"{repo_name:40} {'(no data for user)':>25}")

        if len(repositories) < 100:
            break

        page += 1

    if debug:
        print(
            f"{'TOTAL':40} "
            f"+{total_added:>10,} "
            f"-{total_removed:>10,} "
            f"= {total_added + total_removed:>10,} lines"
        )

    return total_added, total_removed