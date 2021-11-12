"""自定义扩展，实现一个管道，一个爬虫中间件和一个下载器中间件
来战士信号的使用方式"""
import logging

from scrapy import signals
from scrapy.exceptions import DropItem


class HookasyncExtension(object):
    @classmethod
    def from_crawler(cls, crawler):
        logging.info("HookasyncExtension from_crawler")
        return cls(crawler)

    def __init__(self, crawler):
        logging.info("HookasyncExtension Constructor called")

        # 连接扩展对象和信号，下面有11中信号，新版中共有16个
        cs = crawler.signals.connect
        cs(self.engine_started, signal=signals.engine_started)
        cs(self.engine_stopped, signal=signals.engine_stopped)
        cs(self.spider_opened, signal=signals.spider_opened)
        cs(self.spider_idle, signal=signals.spider_idle)
        cs(self.spider_closed, signal=signals.spider_closed)
        cs(self.spider_error, signal=signals.spider_error)
        cs(self.request_scheduled, signal=signals.request_scheduled)
        cs(self.response_received, signal=signals.response_received)
        cs(self.response_downloaded, signal=signals.response_downloaded)
        cs(self.item_scraped, signal=signals.item_scraped)
        cs(self.item_dropped, signal=signals.item_dropped)

    # 定义信号的handler
    def engine_started(self):
        logging.info("HookasyncExtension, signal.engine_started fired")

    def engine_stopped(self):
        logging.info("HookasyncExtension, signals.engine_stopped fired")

    def spider_opened(self, spider):
        logging.info("HookasyncExtension, signals.spider_opened fired")

    def spider_idle(self, spider):
        logging.info("HookasyncExtension, signals.spider_idle fired")

    def spider_closed(self, spider, reason):
        logging.info("HookasyncExtension, signals.spider_closed fired")

    def spider_error(self, failure, response, spider):
        logging.info("HookasyncExtension, signals.spider_error fired")

    def request_scheduled(self, request, spider):
        logging.info("HookasyncExtension, signals.request_scheduled fired")

    def response_received(self, response, request, spider):
        logging.info("HookasyncExtension, signals.response_received fired")

    def response_downloaded(self, response, request, spider):
        logging.info("HookasyncExtension, signals.response_downloaded fired")

    def item_scraped(self, item, response, spider):
        logging.info("HookasyncExtension, signals.item_scraped fired")

    def item_dropped(self, item, spider, exception):
        logging.info("HookasyncExtension, signals.item_dropped fired")

    @classmethod
    def from_settings(cls, settings):
        logging.info("HookasyncExtension from_settings")
        # 这个方法永远不会被调用，但是如果 from_crawler() 不存在则会被调用。
        # from_crawler()可以访问通过crawler.settings访问settings，
        # 也可以访问crawler对象提供的所有信息，如信号、状态和调度crawler.engine.download()的新请求的数量


class HookasyncDownloaderMiddleware(object):
    """下载器中间件是一个中间件，所以他可以做任何中间件可以做的事。
    主要使得他们不同的东西是 process_*() 方法"""

    @classmethod
    def from_crawler(cls, crawler):
        logging.info("HookasyncDownloaderMiddleware from_crawler")
        # 这里的构造器一定会被调用，返回这个类
        return cls(crawler)

    def __init__(self, crawler):
        logging.info("HooksasyncDownloaderMiddleware Constructor called")

    def process_request(self, request, spider):
        logging.info("HookasyncDownloaderMiddleware process_request"
                     "call for %s" % request.url)

    def process_response(self, request, response, spider):
        logging.info("HookasyncDownloaderMiddleware process_response"
                     "called for %s" % request.url)
        return response

    def process_exception(self, request, exception, spider):
        logging.info("HookasyncDownloaderMiddleware process_exception"
                     "called for %s" % request.url)


class HookasyncSpiderMiddleware(object):
    """爬虫中间件是一个中间件，所以他可以做任何中间件可以做的事。
    主要使得他们不同的是 process_*() 方法"""

    @classmethod
    def from_crawler(cls, crawler):
        logging.info("HookasyncSpiderMiddleware from_crawler")
        # 这个构造器一定被调用，返回这个类
        return cls(crawler)

    def __init__(self, crawler):
        logging.info("HooksasyncSpiderMiddleware Constructor called")

    def process_spider_input(self, response, spider):
        logging.info(("HooksasyncSpiderMiddleware process_spider_input "
                      "called for %s") % response.url)

    def process_spider_output(self, response, result, spider):
        logging.info(("HooksasyncSpiderMiddleware process_spider_output "
                      "called for %s") % response.url)
        return result

    def process_spider_exception(self, response, exception, spider):
        logging.info(("HooksasyncSpiderMiddleware process_spider_exception "
                      "called for %s") % response.url)

    def process_start_requests(self, start_requests, spider):
        logging.info("HooksasyncSpiderMiddleware process_start_requests"
                     " called")
        return start_requests


class HookasyncPipeline(object):
    """管道是一个中间件，所以所有中间件可以做的事管道都可以做。
    主要使得他们不同的是他们有 process_item() 方法"""

    @classmethod
    def from_crawler(cls, crawler):
        logging.info("HooksasyncPipeline from_crawler")
        # Here the constructor is actually called and the class returned
        return cls(crawler)

    def __init__(self, crawler):
        logging.info("HooksasyncPipeline Constructor called")

    def process_item(self, item, spider):
        if item['name'] == "Hello 1":
            raise DropItem("Not good")  # 丢弃数据
        logging.info(("HookasyncPipeline process_item() called for"
                      "item: %s" % item['name']))
        return item

    # 该方法重写了item pipelines默认的
    def open_spider(self, spider):
        logging.info("HookasyncPipeline spider_opened")

    # 该方法重写了item pipelines 默认的
    def close_spider(self, spider):
        logging.info("HookasyncPipeline spider_closed")
