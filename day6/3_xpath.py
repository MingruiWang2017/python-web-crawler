from lxml import etree

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<ul>
    <li>1<a href="">一</a></li>
    <li>2<a href="">二</a></li>
    <li>3<a href="">三</a></li>
    <li>4<a href="">四</a></li>
    <li>5<a href="">五</a></li>
</ul>
</body>
</html>
"""

# 1. 转类型
x_data = etree.HTML(html)

# 2.xpath
# 下标从1开始;
result = x_data.xpath('//li[4]/text()') # -->4
print(result)
result = x_data.xpath('//li[4]/a/text()') # -->四
print(result)

# 下标方式只能取平级关系的标签
result = x_data.xpath('//a')
print(len(result))
print(x_data.xpath('//a[2]/text()')) # --> None，a标签不是平级关系
