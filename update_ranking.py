import requests
import os
import time
from datetime import datetime

# 配置分类：键名对应 README 中的标题，值对应 GitHub API 查询语句
CONFIG = {
    "All Categories (Global)": "stars:>1",
    "Python": "language:python stars:>1",
    "JavaScript": "language:javascript stars:>1",
    "TypeScript": "language:typescript stars:>1",
    "Go": "language:go stars:>1",
    "Rust": "language:rust stars:>1",
    "C#": "language:csharp stars:>1",
    "C++": "language:cpp stars:>1",
    "PHP": "language:php stars:>1",
    "HTML": "language:html stars:>1",
    "CSS": "language:css stars:>1",
    "Markdown": "language:markdown stars:>1"
}

TOKEN = os.environ.get("G_TOKEN")
headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

def fetch_data(query):
    # per_page=100 获取前 100 名
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
        return "Data temporarily unavailable."
    
    header = "| Rank | Repo | Stars | Language | Description |\n|:---:|:---|:---:|:---:|:---|\n"
    rows = []
    for i, item in enumerate(items, 1):
        # 为前三名添加奖杯图标
        rank = f"🥇 {i}" if i == 1 else f"🥈 {i}" if i == 2 else f"🥉 {i}" if i == 3 else i
        name = item['full_name']
        url = item['html_url']
        # 格式化 Star 数，例如 123456 -> 123.5k
        stars = f"{item['stargazers_count']/1000:.1f}k"
        lang = item['language'] or "N/A"
        # 截断过长的描述
        desc = item['description'] or "-"
        if len(desc) > 80:
            desc = desc[:77] + "..."
        
        rows.append(f"| {rank} | [{name}]({url}) | {stars} | `{lang}` | {desc} |")
    
    return header + "\n".join(rows)

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # 构建新的 README 内容
    new_content = "# 🌟 GitHub Star Ranking (Top 100)\n\n"
    new_content += f"> **Last Updated:** {now}\n\n"
    new_content += "This list captures the top 100 repositories by star count. Automatically updated daily.\n\n"
    
    # 生成导航栏 (Navigation)
    new_content += "## 🧭 Navigation\n"
    for lang in CONFIG.keys():
        new_content += f"- [{lang}](#-{lang.lower()}-ranking)\n"
    new_content += "\n---\n"

    # 循环抓取数据并生成表格
    for lang, query in CONFIG.items():
        print(f"Processing {lang}...")
        repos = fetch_data(query)
        table = format_table(repos)
        new_content += f"## 🏆 {lang} Ranking\n\n{table}\n\n"
        # 礼貌延时，防止 API 频率限制
        time.sleep(1)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README updated successfully!")

if __name__ == "__main__":
    main()
