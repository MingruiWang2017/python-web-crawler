import json
import dj_redis_url
import txredisapi

from scrapy.exceptions import NotConfigured
from twisted.internet import defer
from scrapy import signals


class RedisCache(object):
    """管道： 使用redis作为键值对缓存"""

    @classmethod
    def from_crawler(cls, crawler):
        # 读取redis url配置
        redis_url = crawler.settings.get("REDIS_PIPELINE_URL", None)
        if not redis_url:
            raise NotConfigured
        # 读取namespace， 这个用作保存到redis中数据key的前缀，用于区分数据
        redis_nm = crawler.settings.get("REDIS_PIPELINE_NS", "ADDRESS_CACHE")

        return cls(crawler, redis_url, redis_nm)

    def __init__(self, crawler, redis_url, redis_nm):
        """保存配置，打开链接并注册回调"""

        # 保存url和namespace
        self.redis_url = redis_url
        self.redis_nm = redis_nm

        # report connection error only one
        self.report_connection_error = True

        # 解析redis url 并初始化连接
        args = RedisCache.parse_redis_url(redis_url)
        self.connection = txredisapi.lazyConnectionPool(connectTimeout=5,
                                                        replyTimeout=5,
                                                        **args)

        # 连接item_scraped 信号
        crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        """在redis缓存中寻找地址"""
        logger = spider.logger

        if "location" in item:
            # 之前步骤已经设置了地理编码，不需要再查询
            defer.returnValue(item)
            return

        # 确保item必须有address字段
        assert ("address" in item) and (len(item["address"]) > 0)

        # 取出地址
        address = item['address'][0]

        try:
            # 检查redis中有没有对应键的缓存
            key = self.redis_nm + ":" + address

            value = yield self.connection.get(key)

            if value:
                # set the value for item
                item['location'] = json.loads(value)

        except txredisapi.ConnectionError:
            if self.report_connection_error:
                logger.error("Can't connect to Redis: %s" % self.redis_url)
                self.report_connection_error = False

        defer.returnValue(item)

    def item_scraped(self, item, spider):
        """该方法在item经过每个管道阶段后检查他们，如果需要添加缓存值，就添加"""
        # 获取并编码location和address
        try:
            location = item['location']
            value = json.dumps(location, ensure_ascii=False)
        except KeyError:  # 如果item中还没有location值，就先忽略，继续通过地理编码管道去查询
            return

        # 如果item中有location字段，则将其缓存进Redis
        # 从item中获取address
        address = item['address'][0]
        key = self.redis_nm + ":" + address

        # twisted.failure.trap() 如果异常的类型在预定的类型列表中，则捕获这个异常。
        # 这允许你在一个错误回调中捕获一个Failure。 如果它不是你所期望的类型，它将被自动重新抛出。
        quiet = lambda failure: failure.trap(txredisapi.ConnectionError)

        # 异步保存在Redis中
        return self.connection.set(key, value).addErrback(quiet)

    @staticmethod
    def parse_redis_url(redis_url):
        """解析 redis url，为txredisapi.lazyConnectionPool准备参数"""

        params = dj_redis_url.parse(redis_url)

        conn_kwargs = {}
        conn_kwargs['host'] = params['HOST']
        conn_kwargs['port'] = params['PORT']
        conn_kwargs['password'] = params['PASSWORD']
        conn_kwargs['dbid'] = params['DB']

        # 移除值为空的字段
        conn_kwargs = dict((k, v) for k, v in conn_kwargs.items() if v)

        return conn_kwargs

# 使用该管道是，开启geo管道，关闭geo2管道
