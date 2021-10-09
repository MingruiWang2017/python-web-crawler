import requests

url = "http://www.baidu.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}

free_proxy = {"http": "47.100.14.22:9006"}

response = requests.get(url, headers=headers, proxies=free_proxy)

print(response.status_code)
