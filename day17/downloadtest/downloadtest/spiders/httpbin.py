import scrapy


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/get']

    def parse(self, response):
        print("=" * 100)
        print(response.status)
        print(response.headers)
        print(response.text)
        print("=" * 100)
