import urllib.request


def proxy_handler():
    # 这里需要使用http的地址， 如果使用https的地址，因为下面使用了HTTP Proxy，会导致不使用代理
    url = "http://blog.csdn.net/qq_37928340/article/details/89278779"

    # 添加代理
    proxy = {
        # 免费代理
        # "http": "http://118.117.188.250:3256"
        "http": "118.117.188.250:3256"
    }
    # 代理的handler
    proxy_handler = urllib.request.ProxyHandler(proxy)

    # 创建opener
    proxy_opener = urllib.request.build_opener(proxy_handler)

    # 使用代理IP请求数据
    res = proxy_opener.open(url)
    data = res.read().decode()

    print(data)


if __name__ == '__main__':
    proxy_handler()
