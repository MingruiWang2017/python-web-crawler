import re
import scrapy
import requests

from scrapy import Request
from urllib import parse
from scrapy.loader import ItemLoader

from ArticleSpider.utils import common
from ArticleSpider.items import ArticlespiderItem, ArticleItemLoader


class CnblogNewsSpider(scrapy.Spider):
    name = 'cnblog_news2'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

    def parse(self, response):
        """
        1. 获取新闻列表页中的新闻url，交给scrapy进行下载后调用相应的解析方法
        2. 获取下一页的url，交给scrapy进行下载，下载后交给parse继续处理
        """
        # 1. 获取详情页url和图片url
        post_nodes = response.css('div#news_list .news_block')
        for post_node in post_nodes:
            front_image_url = post_node.xpath('.//div[@class="entry_summary"]/a/img/@src').get()
            # 部分image的url缺少https:，直接以 // 开头，进行修复
            if front_image_url and not front_image_url.startswith("https"):
                front_image_url = "https:" + front_image_url

            post_url = post_node.css('h2 a::attr(href)').get()
            yield Request(url=parse.urljoin(response.url, post_url),
                          meta={"front_image_url": front_image_url},
                          callback=self.parse_detail)

        # 2. 查找下一页
        # next_url = response.xpath('//a[contains(text(), "Next >")]/@href').get()
        # yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response: scrapy.http.Response):
        """处理详情页"""
        match_re = re.match(".*?(\d+)", response.url)
        if match_re:
            post_id = match_re.groups(1)

            # 使用ItemLoader, 默认ItemLoader构造的item每一项都是列表
            # item_loader = ItemLoader(item=ArticlespiderItem(), response=response)

            # 使用自定义的ArticleItemLoader
            item_loader = ArticleItemLoader(item=ArticlespiderItem(), response=response)

            item_loader.add_xpath('title', '//div[@id="news_title"]/a/text()')
            item_loader.add_xpath('create_date', '//div[@id="news_info"]/span[@class="time"]/text()')
            item_loader.add_xpath('content', '//div[@id="news_content"]')
            item_loader.add_xpath('tags', '//div[@class="news_tags"]/a/text()')
            item_loader.add_value('front_image_url', response.meta.get('front_image_url', ""))
            item_loader.add_value('url', response.url)
            item_loader.add_value('url_md5', common.get_md5(response.url))

            # 换用异步方式
            yield Request(response.urljoin("/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id[0])),
                          meta={'item_loader': item_loader}, callback=self.parse_nums)

    def parse_nums(self, response):
        """获取文章数据"""
        ajax_data = response.json()
        item_loader = response.meta.get('item_loader')

        item_loader.add_value('like_nums', ajax_data['DiggCount'])  # 点赞数
        item_loader.add_value('view_nums', ajax_data['TotalView'])  # 浏览数
        item_loader.add_value('comment_nums', ajax_data['CommentCount'])  # 评论数

        # 异步返回item
        item = item_loader.load_item()  # 获取构造的item
        yield item
