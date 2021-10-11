from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
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
soup = BeautifulSoup(html_doc, features='lxml')  # --> BeautifulSoup

# 2. 解析数据
# 2.1 取标签Tag，使用 . 操作，只能获取第一个标签
head = soup.head
print(head)

p = soup.p
print(p)

a = soup.a
print(a)
print("类型:", type(a))  # --> Tag

print("-" * 40, "\n")
# 2.2 取内容NavigableString
a_content = soup.a.string
print(a_content)
print("类型：", type(a_content))  # --> NavigableString

print("-" * 40, "\n")
# 2.3 取属性
a_href = soup.a['href']
print(a_href)
print("类型：", type(a_href))  # --> str

print("-" * 40, "\n")
# 2.4 取注释Comment
html_doc2 = "<b><!--Hey, buddy. Want to buy a used parser?--></b>"
soup2 = BeautifulSoup(html_doc2, features="html.parser")
b = soup2.b
print(b)

b_str = soup2.b.string
print(b_str)
print("类型： ", type(b_str))  # --> Comment
