import urllib.request
import urllib.error

proxy_list = [
    {"http": "27.191.60.37:3256"},
    {"http": "118.117.188.250:3256"},
    {"http": "114.99.9.39:1133"},
    {"http": "118.117.188.111:3256"},
    {"http": "163.125.249.189:8118"}
]


def get_random_proxy(proxy_index):
    if proxy_index < len(proxy_list):
        proxy = proxy_list[proxy_index]
        proxy_index += 1
        print(proxy)
        return proxy


def proxy_request(proxy_index):
    url = "http://www.baidu.com"
    proxy_handler = urllib.request.ProxyHandler(get_random_proxy(proxy_index))
    proxy_opener = urllib.request.build_opener(proxy_handler)

    try:
        res = proxy_opener.open(url, timeout=10)
        print(res)
    except urllib.error.URLError as e:
        print(e)
    except BaseException as e:
        print(e)


if __name__ == '__main__':
    for proxy_index in range(5):
        proxy_request(proxy_index)
        print("-" * 30)
