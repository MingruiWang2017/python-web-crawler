"""使用DictWriter，json转csv"""

import json
import csv

# 1. 读取json数据
with open('1_articles.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
# 2. 获取表头
sheet_titles = data["projects"][0].keys()

# 3. 使用csv DictWriter写入数据
with open('1_articles-2.csv', 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, sheet_titles)
    # 写入表头
    writer.writeheader()
    # 写入内容
    writer.writerows(data["projects"])