import urllib.request
import urllib.parse

def get_with_params():
    url = "http://www.baidu.com/s?"
    params = {
        "wd": "中文",
        "key": "zhang",
        "value": "san"
    }
    # 将params字典转化为字符串
    str_params = urllib.parse.urlencode(params)  
    # 结果：http://www.baidu.com/s?wd=%E4%B8%AD%E6%96%87&key=zhang&value=san
    final_url = url + str_params
    print(final_url)

    response = urllib.request.urlopen(final_url)
    data = response.read().decode("utf-8")
    print(data)

    with open("1-baidu-get.html", 'w', encoding='utf-8') as f:
        f.write(data)


if __name__ == "__main__":
    get_with_params()