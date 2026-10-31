from __future__ import annotations

import html
import json
import os
import re
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path


USERNAME = "arvazeann"
PROFILE_REPOSITORY = "arvazeann"
ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
OUTPUT = ROOT / "dist" / "active-project.svg"
START_MARKER = "<!-- active-project:start -->"
END_MARKER = "<!-- active-project:end -->"
API = "https://api.github.com"


def api_get(url: str) -> tuple[object, str | None]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "arvazeann-active-project-card",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
        link = response.headers.get("Link")

    next_url = None
    if link:
        match = re.search(r'<([^>]+)>;\s*rel="next"', link)
        if match:
            next_url = match.group(1)
    return payload, next_url


def list_repositories() -> list[dict[str, object]]:
    url = f"{API}/users/{USERNAME}/repos?" + urllib.parse.urlencode(
        {"type": "owner", "sort": "pushed", "direction": "desc", "per_page": 100}
    )
    repositories: list[dict[str, object]] = []
    while url:
        payload, url = api_get(url)
        if not isinstance(payload, list):
            raise RuntimeError("GitHub returned an unexpected repository response")
        repositories.extend(payload)

    return [
        repo
        for repo in repositories
        if repo.get("owner", {}).get("login", "").lower() == USERNAME
        and repo.get("name", "").lower() != PROFILE_REPOSITORY
        and not repo.get("fork")
        and not repo.get("archived")
        and repo.get("visibility", "public") == "public"
    ]


def count_recent_commits(repo: dict[str, object], since: str) -> int:
    full_name = str(repo["full_name"])
    query = urllib.parse.urlencode(
        {"author": USERNAME, "since": since, "per_page": 100}
    )
    url: str | None = f"{API}/repos/{full_name}/commits?{query}"
    count = 0
    while url:
        payload, url = api_get(url)
        if not isinstance(payload, list):
            raise RuntimeError(f"GitHub returned an unexpected commits response for {full_name}")
        count += len(payload)
    return count


def choose_project(repositories: list[dict[str, object]]) -> tuple[dict[str, object], int, str]:
    since_dt = datetime.now(timezone.utc) - timedelta(days=30)
    since = since_dt.isoformat(timespec="seconds").replace("+00:00", "Z")
    recent_repositories = []
    for repo in repositories:
        pushed_at = repo.get("pushed_at")
        if not pushed_at:
            continue
        pushed_dt = datetime.fromisoformat(str(pushed_at).replace("Z", "+00:00"))
        if pushed_dt >= since_dt:
            recent_repositories.append(repo)

    if recent_repositories:
        candidates = [(repo, count_recent_commits(repo, since)) for repo in recent_repositories]
    else:
        # No recent pushes: show the most recently updated public repository with a zero count.
        candidates = [(repo, 0) for repo in repositories]
    if not candidates:
        raise RuntimeError("No eligible public repositories found")

    candidates.sort(
        key=lambda item: (item[1], str(item[0].get("pushed_at", ""))),
        reverse=True,
    )
    repo, count = candidates[0]
    return repo, count, since_dt.strftime("%b %d, %Y").upper()


def clean_text(value: object, limit: int) -> str:
    text = " ".join(str(value or "").split())
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return html.escape(text, quote=False)


def render_svg(repo: dict[str, object], commit_count: int, since_label: str) -> str:
    name = clean_text(repo.get("name", "Project"), 38)
    description = clean_text(repo.get("description") or "Public project from my GitHub repositories.", 80)
    language = clean_text(repo.get("language") or "Multiple technologies", 28)
    if commit_count == 0:
        activity = "No authored commits in this window"
        headline = "LATEST UPDATED PROJECT · NO COMMITS BY ME IN THIS WINDOW"
    elif commit_count == 1:
        activity = "1 commit by me"
        headline = "MOST ACTIVE PROJECT · LAST 30 DAYS"
    else:
        activity = f"{commit_count} commits by me"
        headline = "MOST ACTIVE PROJECT · LAST 30 DAYS"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="220" viewBox="0 0 1000 220" role="img" aria-labelledby="title desc">
  <title id="title">Most active public project: {name}</title>
  <desc id="desc">{activity} since {since_label}; language: {language}. Updated daily from the GitHub API.</desc>
  <rect x="1" y="1" width="998" height="218" rx="14" fill="#0A0F0A" stroke="#174D24" stroke-width="2"/>
  <path d="M1 50H999" stroke="#174D24"/>
  <circle cx="28" cy="26" r="5" fill="#39FF14"/>
  <text x="45" y="31" fill="#83A889" font-family="monospace" font-size="13" letter-spacing="1">{headline}</text>
  <text x="28" y="100" fill="#39FF14" font-family="monospace" font-size="28" font-weight="700">{name}</text>
  <text x="28" y="133" fill="#D5FFD5" font-family="monospace" font-size="15">{description}</text>
  <text x="28" y="181" fill="#83A889" font-family="monospace" font-size="13">{language}  ·  SINCE {since_label}</text>
  <rect x="780" y="70" width="190" height="118" rx="9" fill="#050805" stroke="#174D24"/>
  <text x="875" y="119" text-anchor="middle" fill="#39FF14" font-family="monospace" font-size="31" font-weight="700">{commit_count}</text>
  <text x="875" y="146" text-anchor="middle" fill="#83A889" font-family="monospace" font-size="12">COMMITS BY ME</text>
  <text x="875" y="167" text-anchor="middle" fill="#83A889" font-family="monospace" font-size="10">LAST 30 DAYS</text>
</svg>
'''


def update_readme(repo: dict[str, object]) -> None:
    source = README.read_text(encoding="utf-8")
    if START_MARKER not in source or END_MARKER not in source:
        raise RuntimeError("README is missing the active-project markers")

    full_name = str(repo["full_name"])
    block = f'''{START_MARKER}
<div align="center">
<a href="https://github.com/{html.escape(full_name, quote=True)}">
  <img src="https://raw.githubusercontent.com/{USERNAME}/{PROFILE_REPOSITORY}/output/active-project.svg" width="100%" alt="Most active public project in the last 30 days: {html.escape(str(repo.get('name', 'project')), quote=True)}" />
</a>
</div>
{END_MARKER}'''
    start = source.index(START_MARKER)
    end = source.index(END_MARKER, start) + len(END_MARKER)
    updated = source[:start] + block + source[end:]
    if updated != source:
        README.write_text(updated, encoding="utf-8", newline="\n")


def main() -> None:
    repositories = list_repositories()
    repo, commit_count, since_label = choose_project(repositories)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render_svg(repo, commit_count, since_label), encoding="utf-8", newline="\n")
    update_readme(repo)
    print(f"Selected {repo['full_name']} with {commit_count} authored commits in the last 30 days")


if __name__ == "__main__":
    main()
