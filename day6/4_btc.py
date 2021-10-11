import requests
from lxml import etree
import json


class BtcSpider(object):
    base_url = "https://www.8btc.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }

    def __init__(self, topic=None, pages=1, headers=None):
        if topic:
            self.url = BtcSpider.base_url + "/" + topic
        if headers:
            self.headers = BtcSpider.headers.update(headers)
        self.pages = pages

        self.encoding = None
        self.news_list = []

    # 1.发请求
    def get_response(self):
        response = requests.get(self.url, params=self.params, headers=self.headers)
        self.encoding = response.headers["content-type"].split("charset=")[1]
        # print(self.encoding)
        data = response.content.decode(self.encoding)
        return data

    # 2. 解析数据
    def parse_data(self, data):
        """使用xpath解析当前页面的专题和url"""
        x_data = etree.HTML(data)
        titles = x_data.xpath('//a[@class="link-dark-major"]/text()')
        # print(titles)
        print(len(titles))

        urls = x_data.xpath('//a[@class="link-dark-major"]/@href')
        # print(urls)  # 此时的url不完整，没有基础url，只有文章的编号
        print(len(urls))

        # titles_and_urls = x_data.xpath('//a[@class="link-dark-major"]/@href | //a[@class="link-dark-major"]/text()')
        # print(titles_and_urls)

        # 整合url和标题
        news_list = []
        for url, title in zip(urls, titles):
            news = {}
            url = BtcSpider.base_url + url
            title = title.strip()
            news["url"] = url
            news["title"] = title
            news_list.append(news)
        self.news_list.extend(news_list)
        print(news_list)

    # 3. 保存数据
    def save_data(self, data):
        # with open("4_btc.html", 'w', encoding=self.encoding) as f:
        #     f.write(data)
        with open("4_btc_special.json", 'w', encoding='utf-8') as f:
            json.dump(self.news_list, f, ensure_ascii=False)

    # 4. 启动
    def run(self):
        # 1. 完整的url
        # https://www.8btc.com/special?page=2
        # 共9页
        for i in range(1, self.pages + 1):
            print("page: ", i)
            self.params = {"page": i}

            # 2. 发请求
            data = self.get_response()
            # 3. 解析数据
            self.parse_data(data)
        # 4. 保存
        self.save_data(data)


if __name__ == '__main__':
    btc = BtcSpider("special", pages=9)
    btc.run()
