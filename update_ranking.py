import requests
import os

# 1. 设置 API 请求头 (Token 会在 Action 中注入)
token = os.environ.get("G_TOKEN")
headers = {"Authorization": f"token {token}"} if token else {}

def get_top_50(language=None):
    query = "stars:>1"
    if language:
        query += f" language:{language}"
    
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=50"
    response = requests.get(url, headers=headers)
    return response.json().get('items', [])

# 2. 生成 Markdown 表格字符串
def generate_table(items):
    table = "| Rank | Repo | Stars | Language | Description |\n| :--- | :--- | :--- | :--- | :--- |\n"
    for i, item in enumerate(items, 1):
        name = item['full_name']
        url = item['html_url']
        stars = item['stargazers_count']
        lang = item['language'] or "N/A"
        desc = item['description'] or "No description"
        table += f"| {i} | [{name}]({url}) | {stars} | {lang} | {desc} |\n"
    return table

# 3. 写入 README.md
if __name__ == "__main__":
    all_top = get_top_50()
    content = "# GitHub Global Ranking (Top 50)\n\n" + generate_table(all_top)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
