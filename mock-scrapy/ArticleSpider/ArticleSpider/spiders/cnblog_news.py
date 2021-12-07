import re
import scrapy
import requests

from scrapy import Request
from urllib import parse
from scrapy.loader import ItemLoader

from ArticleSpider.utils import common
from ArticleSpider.items import ArticlespiderItem


class CnblogNewsSpider(scrapy.Spider):
    name = 'cnblog_news'
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
            # 部分image的url缺少https，直接以 // 开头，进行修复
            if front_image_url and not front_image_url.startswith("https"):
                front_image_url = "https:" + front_image_url



            post_url = post_node.css('h2 a::attr(href)').get()
            yield Request(url=parse.urljoin(response.url, post_url),
                          meta={"front_image_url": front_image_url},
                          callback=self.parse_detail)

        # 2. 查找下一页
        # next_page = response.css('div.paper a:last-child::text').get()
        # if next_page == "Next >":
        #     next_url = response.css('div.paper a:last-child::attr(href)').get()
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

        next_url = response.xpath('//a[contains(text(), "Next >")]/@href').get()
        yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response: scrapy.http.Response):
        """处理详情页"""
        title = response.xpath('//div[@id="news_title"]/a/text()').get()
        create_date = response.xpath('//div[@id="news_info"]/span[@class="time"]/text()').get()
        match_re = re.match(".*?(\d+.*)", create_date)
        if match_re:
            create_date = match_re.groups(1)
        content = response.xpath('//div[@id="news_content"]').getall()
        tag_list = response.xpath('//div[@class="news_tags"]/a/text()').getall()
        tags = ",".join(tag_list) if tag_list else ""

        match_re = re.match(".*?(\d+)", response.url)
        if match_re:
            post_id = match_re.groups(1)

            # 不要使用同步的方式进行调用
            # ajax_response = requests.get(
            #     parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id[0])))
            # ajax_data = ajax_response.json()
            # like_nums = ajax_data['DiggCount']  # 点赞数
            # view_nums = ajax_data['TotalView']  # 浏览数
            # comment_nums = ajax_data['CommentCount']  # 评论数

            # 为item赋值
            item = ArticlespiderItem()
            item['title'] = title
            item['create_date'] = create_date
            item['content'] = content
            item['tags'] = tags
            if response.meta.get('front_image_url'):
                item['front_image_url'] = [response.meta.get('front_image_url')]  # 这里必须设置成list，scrapy才能进行下载
            else:
                item['front_image_url'] = []
            item['url'] = response.url
            item['url_md5'] = common.get_md5(response.url)

            # 使用 ItemLoader 方式


            # 换用异步方式
            yield Request(response.urljoin("/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id[0])),
                          meta={'item': item}, callback=self.parse_nums)

    def parse_nums(self, response):
        """获取文章数据"""
        ajax_data = response.json()
        item = response.meta.get('item', {})

        like_nums = ajax_data['DiggCount']  # 点赞数
        view_nums = ajax_data['TotalView']  # 浏览数
        comment_nums = ajax_data['CommentCount']  # 评论数
        item['like_nums'] = like_nums
        item['view_nums'] = view_nums
        item['comment_nums'] = comment_nums

        # 异步返回item
        yield item
