import logging
import json
import treq

from scrapy import signals
from scrapy.http import Request
from twisted.internet import defer
from scrapy.spiders import CrawlSpider
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)


class Distributed(object):

    @classmethod
    def from_crawler(cls, crawler):
        """将crawler直接传给构造方法"""
        return cls(crawler)

    def __init__(self, crawler):
        """初始化爬虫中间件"""

        settings = crawler.settings

        # 也可以使用爬虫的custom_settings来给每个爬虫自定义target rule
        # custom_settings = {
        #     'DISTRIBUTED_TARGET_RULE': 2
        # }
        self._target = settings.getint('DISTRIBUTED_TARGET_RULE', -1)
        if self._target < 0:
            raise NotConfigured


        # 如果设置了以下字段，那么他就是一个工作实例，将会通过下面的URLs开始爬取
        # 而不是用爬虫的start_requests()
        self._start_urls = settings.get('DISTRIBUTED_START_URLS', None)
        self.is_worker = self._start_urls is not None

        # 要被批处理的urls
        self._urls = []

        # 指示要调度到目标scrapyd的下一个批次
        self._batch = 1

        # 批次的大小。默认1000
        self._batch_size = settings.getint('DISTRIBUTED_BATCH_SIZE', 1000)

        # feed uri, 用来使用FTP向spark节点发送数据
        self._feed_uri = settings.get('DISTRIBUTED_TARGET_FEED_URL', None)

        # 目标scraped 主机
        self._targets = settings.get('DISTRIBUTED_TARGET_HOSTS')

        # 作为主节点，没有这些就不能继续操作
        if not self.is_worker:
            if not self._feed_uri or not self._targets:
                raise NotConfigured

        # 连接关闭信号
        crawler.signals.connect(self._closed, signal=signals.spider_closed)

        # 用于在关闭前等待所有scrapyd请求提交完成的列表
        self._scrapyd_submits_to_wait = []

        # 用于url去重的集合
        self._seen = set()

        # project
        self._project = settings.get('BOT_NAME')

    def process_start_requests(self, start_requests, spider):
        """
        如果这是一个工作节点， 他使用来自配置中的 DISTRIBUTED_START_URLS,
        而不是爬虫的start_requests
        """
        if not isinstance(spider, CrawlSpider) or not self.is_worker:
            # 主节点或非活动节点，执行默认操作
            for x in start_requests:
                yield x

        else:
            # 工作节点
            for url in json.loads(self._start_urls):
                # class scrapy.http.Request(url[, callback, method='GET',
                # headers, body, cookies, meta, encoding='utf-8',
                # priority=0, dont_filter=False, errback])
                # Note: This doesn't take into account headers, cookies,
                # non-GET methods etc.只适用于非登录的get请求使用
                yield Request(url, spider._response_downloaded,
                              meta={'rule': self._target})

    def process_spider_output(self, response, result, spider):
        """
        如果请求是发向 target rule的，需要批量处理；否则，直接传过去
        """
        if not isinstance(spider, CrawlSpider) or self.is_worker:
            for x in result:
                yield x

        else:
            for x in result:
                if not isinstance(x, Request):
                    yield x
                else:
                    rule = x.meta.get('rule')

                    if rule == self._target:
                        self._add_to_batch(spider, x)
                    else:
                        yield x

    @defer.inlineCallbacks
    def _closed(self, spider, reason, signal, sender):
        """
        在关闭时，我们要flush所有残留的URLs，同时如果是工作实例，
        还要把所有结果post给spark的流引擎
        """
        # 提交所有残留的URls
        self._flush_urls(spider)

        r = yield defer.DeferredList(self._scrapyd_submits_to_wait)  # 等待所有提交请求完成

        for (success, (debug_data, resp)) in r:
            if not success:
                logger.error("%s: treq request not send" % debug_data)
                continue

            if resp.code != 200:
                body = yield resp.body()
                logger.error("%s: scrapyd request failed: %d. Body: %s" %
                             (debug_data, resp.code, body))
                continue

            ob = yield resp.json()
            if ob['status'] != 'ok':
                logger.error("%s: scrapyd operation %s: %s" %
                             (debug_data, ob['status'], ob))

    def _add_to_batch(self, spider, request):
        """
        添加 Request 的 URL 到批处理数据中。
        如果达到了DISTRIBUTED_BATCH_SIZE, flush 该批次数据
        """
        url = request.url
        if not url in self._seen:  # 去重
            self._seen.add(url)
            self._urls.append(url)
            if len(self._urls) >= self._batch_size:
                self._flush_urls(spider)

    def _flush_urls(self, spider):
        """
        将 urls 刷给目标主机
        """
        if not self._urls:
            return

        target = self._targets[(self._batch - 1) % len(self._targets)]  # 获取目标主机

        logger.info("Posting batch %d with %d URLs to %s",
                    self._batch, len(self._urls), target)

        # 准备发送给scrapyd的请求数据，用于启动爬虫
        data = [
            ("project", self._project),
            ("spider", spider.name),
            ("setting", "FEED_URI=%s" % self._feed_uri),
            ("batch", str(self._batch)),
        ]

        debug_data = "target (%d): %s" % (len(self._urls), data)

        json_urls = json.dumps(self._urls)
        data.append(("setting", "DISTRIBUTED_START_URLS=%s" % json_urls))

        # 发送数据给scrapyd schedule.json，启动爬虫
        d = treq.post('http://%s/schedule.json' % target,
                      data=data, timeout=5, persistent=False)

        d.addBoth(lambda resp: (debug_data, resp))

        # 将请求延迟加入到等待列表中
        self._scrapyd_submits_to_wait.append(d)

        # 为下一批次清空当前数据
        self._urls = []
        self._batch += 1
