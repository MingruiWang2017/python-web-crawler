import scrapy
import datetime
import socket

from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose
from ..items import PropertiesItem


class BasicSpider(scrapy.Spider):
    name = 'manual'
    allowed_domains = ['192.168.73.130']
    start_urls = ['http://192.168.73.130:9312/properties/index_00000.html']

    def parse_item(self, response):
        """
        #设置check使用的contract#
        @url http://192.168.73.130:9312/properties/property_000000.html
        @returns items 1
        @scrapes title price description address image_urls
        @scrapes url project spider server date
        """
        # 使用ItemLoader
        l = ItemLoader(item=PropertiesItem(), response=response)

        l.add_xpath('title', '//*[@itemprop="name"][1]/text()',
                    MapCompose(str.strip, str.title))
        l.add_xpath('price', '//*[@itemprop="price"][1]/text()',
                    MapCompose(lambda i: i.replace(',', ''), float), re='[,.0-9]+')
        l.add_xpath('description', '//*[@itemprop="description"][1]/text()',
                    MapCompose(str.strip), Join())
        l.add_xpath('address', '//*[@itemtype="http://schema.org/Place"][1]/text()',
                    MapCompose(str.strip))
        l.add_xpath('image_urls', '//*[@itemprop="image"][1]/@src',
                    MapCompose(lambda i: response.urljoin(i)))

        # 其他直接取值的字段
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()

    def parse(self, response):
        # Get the next index URLs and yield Requests
        next_selector = response.xpath('//*[contains(@class, "next")]//@href')

        for url in next_selector.extract():
            yield Request(response.urljoin(url))

        # Get item URLs and yield Requests
        item_selector = response.xpath('//*[@itemprop="url"]/@href')
        for url in item_selector.extract():
            yield Request(response.urljoin(url),
                          callback=self.parse_item)