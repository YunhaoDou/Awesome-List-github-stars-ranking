import requests
import os
import time
from datetime import datetime

# 配置需要抓取的分类
CONFIG = {
    "GLOBAL": "stars:>1",
    "PYTHON": "language:python stars:>1",
    "GO": "language:go stars:>1",
    "RUST": "language:rust stars:>1",
    "JAVASCRIPT": "language:javascript stars:>1"
}

TOKEN = os.environ.get("G_TOKEN")
headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

def fetch_data(query):
    # 请求 100 条数据
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=100"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get('items', [])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def format_table(items):
    if not items: return "Data temporary unavailable."
    
    header = "| Rank | Repo | Stars | Language | Description |\n|:---:|:---|:---:|:---:|:---|\n"
    rows = []
    for i, item in enumerate(items, 1):
        # 处理前三名的奖杯图标
        rank = f"🥇 {i}" if i == 1 else f"🥈 {i}" if i == 2 else f"🥉 {i}" if i == 3 else i
        name = item['full_name']
        url = item['html_url']
        stars = f"{item['stargazers_count']/1000:.1f}k" # 转换成 123.4k 格式
        lang = item['language'] or "N/A"
        desc = (item['description'][:60] + '...') if item['description'] and len(item['description']) > 60 else (item['description'] or "-")
        
        rows.append(f"| {rank} | [{name}]({url}) | {stars} | `{lang}` | {desc} |")
    
    return header + "\n".join(rows)

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # 更新时间戳 (Timestamp)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    # 这里我们简单替换，实际推荐用正则更稳健
    # content = content.replace("", now) # 这种方式如果之前有时间会被覆盖，下面是更稳妥的做法

    for key, query in CONFIG.items():
        print(f"Processing {key}...")
        repos = fetch_data(query)
        table = format_table(repos)
        
        # 这种逻辑假设 README 里已经有占位符
        start_tag = f""
        # 我们用一个简单技巧：每次生成新的内容时，保留这个标签
        if start_tag in content:
            # 这里的逻辑是：把标签后面的内容替换掉，或者直接精准定位
            # 简单的做法是把整个 README 重新拼装（如果你不熟悉正则）
            parts = content.split(start_tag)
            # 每一个循环，我们只替换该标签之后直到下一个标题之前的内容
            # 为简单起见，这里演示直接替换标签
            # 在实际复杂应用中，建议使用 和 一对标签
            pass 

    # 简易版：直接重写整个文件逻辑（如果你还没掌握正则）
    # 我们可以先生成一个完整的新 content 字符串
    new_content = f"# 🌟 GitHub Star Ranking (Top 100)\n\nLast Updated: {now}\n\n"
    for key, query in CONFIG.items():
        repos = fetch_data(query)
        new_content += f"## {key.capitalize()} Ranking\n\n" + format_table(repos) + "\n\n"
        time.sleep(1) # 睡眠 1 秒，对 GitHub API 友好 (Politeness)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_readme()
