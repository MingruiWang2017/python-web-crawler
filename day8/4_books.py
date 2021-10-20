"""爬取国外电子书网站内容"""
import requests
import json
import time
from lxml import etree
from bs4 import BeautifulSoup


class BookSpider(object):

    def __init__(self):
        self.base_url = "https://foxgreat.com/search/python/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
            "Cookie": "X_CACHE_KEY=dde53911cde1167b4d1046ce73cbe0e2; _gid=GA1.2.76346632.1634702705; _ga_RPDBM441Z1=GS1.1.1634714170.3.1.1634715046.0; _ga=GA1.2.430025732.1634702705"
        }
        self.data = []

    def get_number_of_pages(self):
        """获取共有多少页"""
        url = self.base_url.format(1)
        response = requests.get(url, headers=self.headers)
        page_data = etree.HTML(response.content.decode())
        page_number = page_data.xpath('//span[@class="page-link"]/text()')[0] \
            .split()[-1]
        print("total pages: ", page_number)
        return int(page_number)

    def get_url_list(self, pages):
        """1. 构建所有页数的url"""
        url_list = []
        for page in range(1, pages + 1):
            url = self.base_url.format(page)
            url_list.append(url)
        return url_list

    def send_request(self, url):
        """2. 发送请求"""
        return requests.get(url, headers=self.headers)

    def parse_xpath_data(self, response):
        """3. 使用xpath解析数据"""
        data = etree.HTML(response.content.decode())
        books = data.xpath('//div[@class="card"]')
        # 1. 解析出每一本书
        for book in books:
            # 2. 解析每本书的信息：书名，作者，发布日期，图片的url
            book_name = book.xpath('.//a[@rel="bookmark"]/text()')[0]  # 在当前节点路径上继续搜索（二次解析）
            author = book.xpath('.//a[@rel="tag"]/text()')  # 可能有多名作者
            try:
                publish_date = book.xpath('.//meta[@itemprop="datePublished"]/@content')[0]
            except Exception:
                publish_date = []
            cover = book.xpath('.//img/@data-src')[0]
            self.data.append({
                "book_name": book_name,
                "author": author,
                "publication_date": publish_date,
                "cover": cover
            })

    def parse_bs_data(self, response):
        """3。 使用bs解析数据"""
        soup = BeautifulSoup(response.content.decode(), 'lxml')
        books = soup.select('.card div[class="row no-gutters shadow"]')

        # 1.解析出每一本书
        for book in books:
            # 2. 解析每本书的信息：书名，作者，发布日期，图片的url
            book_name = book.select_one('a[rel="bookmark"]').get_text()  # 在当前节点路径上继续搜索（二次解析）
            author = []
            for a in book.select('a[rel="tag"]'):
                author.append(a.get_text())  # 可能有多名作者
            try:
                publish_date = book.select_one('meta[itemprop="datePublished"]').get("content")
            except Exception:
                publish_date = []
            cover = book.select_one('img').get("data-src")
            self.data.append({
                "book_name": book_name,
                "author": author,
                "publication_date": publish_date,
                "cover": cover
            })


    def save_data(self, data):
        """4. 保存数据, 追加"""
        print("saving data...")
        with open("4_books.json", 'r', encoding='utf-8') as f:
            if f.read():
                f.seek(0)  # 将游标移动会开头
                data = json.load(f)
            else:
                data = []
        with open("4_books.json", 'w', encoding='utf-8') as f:
            data.extend(self.data)
            json.dump(data, f)

    # 统一调用
    def start(self):
        pages = self.get_number_of_pages()
        url_list = self.get_url_list(pages)

        try:
            i = 1
            for url in url_list:
                i += 1
                response = self.send_request(url)
                if response.status_code == 200:
                    print("getting page ", url)
                    # self.parse_xpath_data(response)
                    self.parse_bs_data(response)
                # 每10页保存一次数据，同时把self.data清空，防止重复存入相同数据
                if i % 5 == 0:
                    self.save_data(self.data)
                    time.sleep(2)
                    self.data = []
        except Exception as e:
            print(e.with_traceback())
        self.save_data(self.data)


if __name__ == '__main__':
    book = BookSpider()
    book.start()
