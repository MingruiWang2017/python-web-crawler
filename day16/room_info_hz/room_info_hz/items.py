# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RoomInfoHzItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()  # 租金
    address = scrapy.Field()
    area = scrapy.Field()  # 面积
    floor = scrapy.Field()  # 楼层
    house_type = scrapy.Field()  # 户型:一室一厅
    rent_type = scrapy.Field()  # 出租类型：合租/整租
    other = scrapy.Field()  # 其他信息
