import requests

url = "https://12306.cn"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}

# 因为https 是由第三方CA证书认证的
# 但是12306虽然是 https 但是他不是CA证书，是自己颁发的证书
# 解决方法是：告诉web忽略 SSL 证书

# 报错：requests.exceptions.SSLError: HTTPSConnectionPool(host='12306.cn', port=443):
# Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError...))
try:
    response = requests.get(url, headers=headers)
except requests.exceptions.RequestException as e:
    print(e)

# 忽略 SSL 证书认证
response = requests.get(url, headers=headers, verify=False)


with open("3_ssl.html", "wb") as f:
    f.write(response.content)
