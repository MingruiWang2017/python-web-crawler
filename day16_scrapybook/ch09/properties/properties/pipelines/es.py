import json
import treq

from urllib.parse import quote
from twisted.internet import defer
from scrapy.exceptions import NotConfigured
from twisted.internet.error import ConnectError
from twisted.internet.error import ConnectingCancelledError


class EsWriter(object):
    """管道：将数据写入ElasticSearch"""

    @classmethod
    def from_crawler(cls, crawler):
        """create a new instance and pass ti ES's url"""

        # 从settings中获取ES配置的url
        es_url = crawler.settings.get("ES_PIPELINE_URL", None)

        if not es_url:
            raise NotConfigured

        return cls(es_url)

    def __init__(self, es_url):
        """store url and initialize error reporting"""

        self.es_url = es_url

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        """
        管道主方法，使用 inlineCallbacks 来发送异步POST请求给ES
        :param item:
        :param spider:
        :return:
        """
        try:
            # 将item装换位json数据作为请求的body
            data = json.dumps(dict(item), ensure_ascii=False).encode('utf-8')
            # 使用treq异步发送POST请求
            yield treq.post(self.es_url, data, timeout=5)
        finally:
            # in any case, return the dict for the next stage
            defer.returnValue(item)