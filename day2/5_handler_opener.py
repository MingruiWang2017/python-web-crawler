import urllib.request


def handler_opener():
    # 系统的urlopen并没有添加代理的功能，需要我们自定义handler
    # ssl 安全套接层，使用第三方CA数字证书
    # http:80端口；https:443端口

    # openurl为什么可以请求数据： handler处理器
    # context --> handler --> opener -- opener.open请求数据

    url = "https://blog.csdn.net/qq_37928340/article/details/89278779"

    # 创建自己的handler
    handler = urllib.request.HTTPHandler()
    # 创建自己的opener
    opener = urllib.request.build_opener(handler)
    # 用自己创建的opener调用open方法请求数据
    res = opener.open(url)

    data = res.read().decode("utf-8")

    print(res)
    print(data)


if __name__ == '__main__':
    handler_opener()
