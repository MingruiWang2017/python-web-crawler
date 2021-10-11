import requests
import re
import os
import pprint

# 使用正则匹配网页内容

# 获取百度新闻网页内容
url = "http://news.baidu.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}
response = requests.get(url, headers=headers)
data = response.content.decode()

if not os.path.isfile(os.path.join(os.getcwd(), "1_news.html")):
    with open("1_news.html", 'w', encoding='utf-8') as f:
        f.write(data)

# 使用正则匹配每个新闻的标题和url
# <a href="http://baijiahao.baidu.com/s?id=1713039671516396061" mon="ct=1&amp;a=2&amp;c=top&pn=11" target="_blank">为做好电力保供，国庆假期多省省委书记或省长去电网公司 </a>

# pattern = re.compile('<a href=\"(.*)\" mon.*_blank\">(.*)</a>')
pattern = re.compile('<a href=\"(?P<url>.*)\" .*target.*>(?P<title>.*)</a>')
# 匹配效果不好……
result = pattern.findall(data)
print(len(result))
pprint.pprint(result)
