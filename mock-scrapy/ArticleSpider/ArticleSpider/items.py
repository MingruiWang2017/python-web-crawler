# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst, Identity, Join


def add_article(value):
    return "article: " + value


def date_convert(value):
    match_re = re.match('.*?(\d+.*)', value)
    if match_re:
        return match_re.group(1)
    else:
        return "1970-07-01"


class ArticlespiderItem(Item):
    title = Field(
        input_processor=MapCompose(add_article)  # 对title字段执行指定的方法
    )
    create_date = Field(
        input_processor=MapCompose(date_convert)  # 提取时间
    )
    url = Field()
    url_md5 = Field()
    front_image_url = Field(
        output_processor=Identity()
    )
    front_image_path = Field()
    like_nums = Field()
    comment_nums = Field()
    view_nums = Field()
    tags = Field(
        input_processor=Join(separator=', ')  # 将list转换为连接的string
    )
    content = Field()


class ArticleItemLoader(ItemLoader):
    # 将默认输入处理器设置为获取第一个元素
    default_output_processor = TakeFirst()
