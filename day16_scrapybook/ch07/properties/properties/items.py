# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class PropertiesItem(Item):
    # 主要字段
    title = Field()
    price = Field()
    description = Field()
    address = Field()
    image_urls = Field()

    # 次要字段
    images = Field()
    location = Field()

    # 服务相关字段
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()
