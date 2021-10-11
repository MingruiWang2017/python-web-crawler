from bs4 import BeautifulSoup

html_doc = """
<html><head><title id="one">The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

# 1. 转换文档解析类型
soup = BeautifulSoup(html_doc, features='lxml')

# 2. 通用解析方法，获取所有数据

# find: 返回符合查询条件的第一个Tag
p = soup.find(name="p")
print("1: ", p)
p = soup.find(attrs={"class": "story"})
print("2: ", p)

a = soup.find(name="a")
print("3: ", a)
a = soup.find(name="a", attrs={"id": "link3"})
print("4: ", a)

a = soup.find(text="Lacie")
print("5: ", a)

print("-" * 50, "\n")

# fina_all: List 所有符合条件的Tag
a = soup.find_all(name='a')
print("1: ", a)
a = soup.find_all(name='a', limit=1)
print("2: ", a)

print("-" * 50, "\n")

# select_one: 需要css选择器, 返回第一个
# class选择器
a = soup.select_one('.sister')
print("1: ", a)
# ID选择器
title = soup.select_one('#one')
print("2: ", title)
# 后代选择器
child = soup.select_one('head title')
print("3: ", child)
# 组选择器
group = soup.select_one('title,.title')
print("4: ", group)
# 属性选择器
attr = soup.select_one('a[id="link3"]')
print("5: ", attr)

print("-" * 50, "\n")

# select: 返回所有--list
# class选择器
a = soup.select('.sister')
print("1: ", a)
# ID选择器
title = soup.select('#one')
print("2: ", title)
# 后代选择器
child = soup.select('head title')
print("3: ", child)
# 组选择器
group = soup.select('title,.title')
print("4: ", group)
# 属性选择器
attr = soup.select('a[id="link3"]')
print("5: ", attr)

print("-" * 50, "\n")

# 获取标签包裹的内容
content = soup.select('b')[0].get_text()
print(content)
content = soup.select('b')[0].string
print(content)

# 获取标签的属性
attr = soup.select('#link1')[0].get('href')
print(attr)