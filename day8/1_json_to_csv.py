"""json转csv"""
import json
import csv

# 1. 分别 读取、创建文件
json_f = open('1_articles.json', 'r', encoding='utf-8')
csv_f = open('1_articles.csv', 'w', encoding='utf-8')

# 2. 提出 表头、文件内容
data = json.load(json_f)
sheet_title = data["projects"][0].keys()
sheet_data = []
for d in data["projects"]:
    sheet_data.append(d.values())

# 3. csv写入器
writer = csv.writer(csv_f)
# 4. 写入表头
writer.writerow(sheet_title)
# 5. 写入内容
writer.writerows(sheet_data)

# 6. 关闭两个文件
json_f.close()
csv_f.close()
