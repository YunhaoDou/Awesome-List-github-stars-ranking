import re
import requests
import os
import time
from datetime import datetime

# (display_name, search_query)
# 用 "C Sharp" / "C Plus Plus" 而非 "C#" / "C++",避免 GitHub 锚链接处理特殊字符的歧义
LANGUAGES = [
    ("All Categories",  "stars:>1"),
    ("Python",          "language:python stars:>1"),
    ("JavaScript",      "language:javascript stars:>1"),
    ("TypeScript",      "language:typescript stars:>1"),
    ("Go",              "language:go stars:>1"),
    ("Rust",            "language:rust stars:>1"),
    ("C Sharp",         "language:csharp stars:>1"),
    ("C Plus Plus",     "language:cpp stars:>1"),
    ("PHP",             "language:php stars:>1"),
    ("HTML",            "language:html stars:>1"),
    ("CSS",             "language:css stars:>1"),
    ("Markdown",        "language:markdown stars:>1"),
]

TOKEN = os.environ.get("G_TOKEN")
headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}


def slugify(text):
    """GitHub-style anchor: lowercase, spaces to hyphens, strip non word/hyphen."""
    s = text.lower()
    s = s.replace(' ', '-')
    s = re.sub(r'[^\w\-]', '', s)
    return s


def fetch_data(query):
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=100"
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json().get('items', [])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []


def format_table(items):
    if not items:
        return "Data temporarily unavailable.\n"
    header = "| Rank | Repository | Stars | Language | Description |\n|:---:|:---|:---:|:---:|:---|\n"
    rows = []
    for i, item in enumerate(items, 1):
        name = item['full_name']
        url = item['html_url']
        stars = f"{item['stargazers_count']/1000:.1f}k"
        lang = item['language'] or "N/A"
        desc = item['description'] or "-"
        desc = desc.replace('\n', ' ').replace('|', '\\|')
        if len(desc) > 80:
            desc = desc[:77] + "..."
        rows.append(f"| {i} | [{name}]({url}) | {stars} | `{lang}` | {desc} |")
    return header + "\n".join(rows) + "\n"


def main():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines.append("# GitHub Star Ranking")
    lines.append("")
    lines.append("[![Update Ranking](https://github.com/YunhaoDou/Awesome-List-github-stars-ranking/actions/workflows/main.yml/badge.svg)](https://github.com/YunhaoDou/Awesome-List-github-stars-ranking/actions/workflows/main.yml)")
    lines.append("[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)")
    lines.append("[![Last Commit](https://img.shields.io/github/last-commit/YunhaoDou/Awesome-List-github-stars-ranking)](https://github.com/YunhaoDou/Awesome-List-github-stars-ranking/commits/main)")
    lines.append("")
    lines.append(f"> **Last Updated:** {now}")
    lines.append("")
    lines.append("Top 100 GitHub repositories by star count, globally and per language. Auto-refreshed every 6 hours via GitHub Actions.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Navigation with proper anchors
    lines.append("## Navigation")
    lines.append("")
    for display, _ in LANGUAGES:
        anchor = slugify(display + "-ranking")
        lines.append(f"- [{display}](#{anchor})")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Sections
    for display, query in LANGUAGES:
        print(f"Processing {display}...")
        repos = fetch_data(query)
        table = format_table(repos)
        lines.append(f"## {display} Ranking")
        lines.append("")
        lines.append(table)
        lines.append("")
        time.sleep(1)

    # Footer / About
    lines.append("---")
    lines.append("")
    lines.append("## About")
    lines.append("")
    lines.append("Automated ranking of public GitHub repositories by star count. Rankings are queried from the GitHub Search API every 6 hours by a scheduled GitHub Action.")
    lines.append("")
    lines.append("**Caveats**")
    lines.append("")
    lines.append("- Star count is a noisy popularity proxy, not a substitute for quality assessment")
    lines.append("- Some repositories rank high due to viral moments rather than sustained usefulness")
    lines.append("- Languages are based on GitHub's auto-detected primary language, which can mis-classify polyglot repos")
    lines.append("- This list ranks by total stars, not recent growth - use [GitHub Trending](https://github.com/trending) for that")
    lines.append("")
    lines.append("## License")
    lines.append("")
    lines.append("[MIT](LICENSE)")
    lines.append("")

    content = "\n".join(lines)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("README updated successfully!")


if __name__ == "__main__":
    main()
