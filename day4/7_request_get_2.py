# 使用requests库发送get请求不需要手动转译
import requests

# 中文可以自动转译
url = "http://www.baidu.com/s?wd=北京"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}

response = requests.get(url, headers=headers)
data = response.content

with open("7_requests_get_1.html", 'wb') as f:
    f.write(data)

print(response.url)

print("=" * 30)
# 使用字典传参，自动拼接参数
url = "http://www.baidu.com/s"
params = {
    "wd": "北京"
}

response = requests.get(url, params, headers=headers)
data = response.content
with open("7_requests_get_2.html", 'wb') as f:
    f.write(data)
print(response.url)

