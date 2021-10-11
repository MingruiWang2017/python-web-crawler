import requests
from lxml import etree

# 获取网页数据
url = "http://news.baidu.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}
response = requests.get(url, headers=headers)
data = response.content.decode()

# 1. 转解析类型
xpath_data = etree.HTML(data)

# xpath 语法：
#       1. 节点: /
#       2. 跨节点：//
#       3. 精确的标签：//a[@属性="属性值"]
#       4. 标签包裹的内容： text()
#       5. 取属性： @，如@href
# Xpath 返回类型： List

# 2. 调用xpath的方法
result = xpath_data.xpath('/html/head/title/text()')
print(result)

result = xpath_data.xpath('//a/text()')
print(result)

# 查找mon 属性在网页源码中为 ct=1&amp;a=2&amp;c=top&pn=21 的标签
# 其中 &amp; 代表HTMl中 & 符号的转义字符，需要将其改为 &

# result = xpath_data.xpath('//a[@mon="ct=1&amp;a=2&amp;c=top&pn=21"]/text()') # --> None
result = xpath_data.xpath('//a[@mon="ct=1&a=2&c=top&pn=21"]/text()')
print(result)

result = xpath_data.xpath('//a[@mon="ct=1&a=2&c=top&pn=13"]/@href')
print(result)
