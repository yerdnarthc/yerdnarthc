# ascii_profile/src/ascii_converter/github.py

import json
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .profile import GitHubStats


GITHUB_API = "https://api.github.com"
GITHUB_GRAPHQL_API = "https://api.github.com/graphql"


def _get_json(url: str, headers: dict[str, str], params: dict[str, int] | None = None):
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
):
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
) -> GitHubStats:
    headers = {
        "Accept": "application/vnd.github+json",
    }

    user = _get_json(
        f"{GITHUB_API}/users/{username}",
        headers=headers,
    )

    repositories = user["public_repos"]
    followers = user["followers"]

    stars = get_total_stars(username, headers)

    commits = get_commit_count(username, token, start, end)

    return GitHubStats(
        repositories=repositories,
        commits=commits,
        stars=stars,
        followers=followers,
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
                "per_page": 100,
                "page": page,
            },
        )

        if not repositories:
            break

        total += sum(
            repo["stargazers_count"]
            for repo in repositories
        )

        if len(repositories) < 100:
            break

        page += 1

    return total


def get_commit_count(
    username: str,
    token: str,
    start: datetime | None = None,
    end: datetime | None = None,
) -> int:
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
                totalCommitContributions
            }
        }
    }
    """

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    if start is None:
        start = datetime(2008, 1, 1, tzinfo=timezone.utc)
    if end is None:
        end = datetime.now(timezone.utc)

    total_commits = 0

    while start < end:
        # GitHub requires the span to be no more than one year.
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

        try:
            commits = result["data"]["user"]["contributionsCollection"][
                "totalCommitContributions"
            ]
        except (KeyError, TypeError):
            raise RuntimeError(f"Unexpected GitHub response: {result}")

        total_commits += commits

        start = next_end

    return total_commits