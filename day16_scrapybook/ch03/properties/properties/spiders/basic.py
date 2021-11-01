import scrapy
import datetime
import socket

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose
from ..items import PropertiesItem


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['192.168.73.130']
    start_urls = ['http://192.168.73.130:9312/properties/property_000000.html']

    def parse(self, response):
        """
        #设置check使用的contract#
        @url http://192.168.73.130:9312/properties/property_000000.html
        @returns items 1
        @scrapes title price description address image_urls
        @scrapes url project spider server date
        """


        # 仅打印日志
        # self.log("title: %s" % response.xpath(
        #     '//*[@itemprop="name"][1]/text()').get())
        # self.log("price: %s" % response.xpath(
        #     '//*[@itemprop="price"][1]/text()').re('[.0-9]+'))
        # self.log("description: %s" % response.xpath(
        #     '//*[@itemprop="description"][1]/text()').getall())
        # self.log("address: %s" % response.xpath(
        #     '//*[@itemtype="http://schema.org/Place"][1]/text()').get())
        # self.log("image_urls: %s" % response.xpath(
        #     '//*[@itemprop="image"][1]/@src').getall())

        # 直接实例化 item，存储数据
        # item = PropertiesItem()
        # item['title'] = response.xpath('//*[@itemprop="name"][1]/text()').get()
        # item['price'] = response.xpath('//*[@itemprop="price"][1]/text()').re('[.0-9]+')
        # item['description'] = response.xpath('//*[@itemprop="description"][1]/text()').getall()
        # item['address'] = response.xpath('//*[@itemtype="http://schema.org/Place"][1]/text()').get()
        # item['image_urls'] = response.xpath('//*[@itemprop="image"][1]/@src').getall()
        #
        # return item

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