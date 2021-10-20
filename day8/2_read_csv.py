import csv

with open("1_articles.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for i in reader:
        if i:
            print(i)