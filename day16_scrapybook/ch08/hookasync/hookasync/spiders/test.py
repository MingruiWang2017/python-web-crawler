from scrapy.spiders import Spider
from scrapy.item import Item, Field


class HookasyncItem(Item):
    name = Field()


class TestSpider(Spider):
    """该项目使用的爬虫非常简单，只对两个item进行yield 操作，然后抛出异常。"""
    name = 'test'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        for i in range(2):
            item = HookasyncItem()
            item['name'] = "Hello %d" % i
            yield item
        raise Exception("dead")
