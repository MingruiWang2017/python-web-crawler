import urllib.request


def load_data():
    url = "http://www.baidu.com"
    # get 请求
    response = urllib.request.urlopen(url)
    print(response)
    # 读取内容
    data = response.read()
    print(data)
    # 将数据转换为字符串
    data_str = data.decode('utf-8')
    print(data_str)
    # 将数据写入文件
    with open('1-baidu.html', 'w', encoding='utf-8') as f:
        f.write(data_str)

    # 将字符串类型转换为bytes
    str_name = "baidu"
    bytes_name = str_name.encode('utf-8')
    print(bytes_name)

    # python 爬取的类型： bytes str
    # 如果爬取过来的是bytes类型，但是写入的时候需要写入字符串：data.decode('utf-8')
    # 如果爬取过来的是str类型， 但是写入的时候要写如为bytes类型：data.encode('utf-8')


if __name__ == '__main__':
    load_data()