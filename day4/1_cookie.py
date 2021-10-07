import urllib.request

# 1. 请求url
url = "https://www.yaozh.com/member/"
# rui_medicine
# Medicine_RUI@123

# 2.添加请求头
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}
# 3.构建请求对象
req = urllib.request.Request(url, headers=header)
#  4. 发送请求
res = urllib.request.urlopen(req)

data = res.read()

with open("1_yaozh_without_cookie.html", 'wb') as f:
    f.write(data)
