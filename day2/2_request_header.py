import urllib.request
import urllib.parse
import string



def load_baidu():
    url = "http://www.baidu.com"

    response = urllib.request.urlopen(url)
    print("响应header信息：")
    print(response.headers)

    print("-"*100)
    # 创建请求对象
    req = urllib.request.Request(url)
    # 请求网络数据
    res = urllib.request.urlopen(req)
    print("请求头信息：")
    print(req.headers)  # 此时请求头信息为空{}
    print("响应头信息：")
    print(res.headers)

    data = response.read().decode("utf-8")
    with open("2-baidu.html", "w", encoding="utf-8") as f:
        f.write(data)


if __name__ == '__main__':
    load_baidu()