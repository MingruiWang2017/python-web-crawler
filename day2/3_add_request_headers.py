import urllib.request

def load_baidu_http():
    url = "http://www.baidu.com"

    response = urllib.request.urlopen(url)
    data = response.read()
    with open("3_baidu_http.html", 'wb') as f:
        f.write(data)

def load_baidu_https():
    url = "https://www.baidu.com"

    # 自定义headers
    headers = {
        # 浏览器信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "haha": "hehe"
    }
    # 创建请求对象
    req = urllib.request.Request(url, headers=headers)
    print("所有请求头信息：")
    print(req.headers)
    print("-" * 100)

    print("获取某个 header 信息：")
    # 注意点：第一个字母大写，其他字母需要小写
    print(req.get_header("User-Agent"))
    print(req.get_header("User-agent"))
    print(req.get_header("haha"))
    print(req.get_header("Haha"))

    # 此时request添加和User-Agent头，便可以请求打开https的百度地址了
    res = urllib.request.urlopen(req)
    data = res.read().decode("utf-8")
    with open("3_baidu_https.html", 'w', encoding="utf-8") as f:
        f.write(data)

def load_baidu_https2():
    '''动态添加headers'''
    url = "https://www.baidu.com"
    req = urllib.request.Request(url)
    # 动态添加所需要的header
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36")
    print(req.headers)

    # 查看完整的url
    full_url = req.get_full_url()
    print("full_url: ", full_url)

    res = urllib.request.urlopen(req)
    data = res.read()
    with open("3_baidu_https2.html", 'wb') as f:
        f.write(data)


if __name__ == '__main__':
    load_baidu_https2()
