import urllib.parse
import urllib.request
import string


def get_with_params():
    url = "http://www.baidu.com/s?wd="
    params = "爬虫"

    full_url = url + params
    print(full_url)

    # 因为url中包含汉字，但是url的使用US-ascii码不支持汉字，进行进行转换
    final_url = urllib.parse.quote(full_url, safe=string.printable)
    print(final_url)
    # python可以接收的url格式：
    # http://www.baidu.com/s?wd=%E7%88%AC%E8%99%AB

    # 发送请求
    response = urllib.request.urlopen(final_url)
    data = response.read().decode()
    print(data)

    # 保存数据
    with open("2-baidu-爬虫.html", 'w', encoding='utf-8') as f:
        f.write(data)


if __name__ == '__main__':
    get_with_params()

