import traceback
import treq

from twisted.internet import defer


class GeoPipeline(object):
    """该管道用来查询地址对应的坐标, 为item添加属性"""

    @classmethod
    def from_crawler(cls, crawler):
        """Create a new instance and pass it crawler's stat object"""
        return cls(crawler.stats)

    def __init__(self, stats):
        """Initialize empty cache and stats object"""
        self.stats = stats

    @defer.inlineCallbacks
    def geocode(self, address):
        """
        The method makes a call to Google's geocode API.
        You shouldn't call thos more than 5 times per second
        """
        # API的url，这里使用假的API来快速返回结果
        # endpoint = "http://maps.googleapis.com/maps/api/geocode/json"
        endpoint = "http://192.168.73.130:9312/maps/api/geocode/json"

        # 发送请求
        params = [('address', address), ('sensor', 'false')]
        response = yield treq.get(endpoint, params=params)

        # 解析返回结果
        content = yield response.json()

        if content['status'] != "OK":
            raise Exception("Unexpected status=\"%s \" for address=\"%s \"" %
                            (content["status"], address))

        geo = content['results'][0]['geometry']['location']

        # 返回结果
        defer.returnValue({"lat": geo["lat"], "lon": geo["lng"]})

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        """
        管道的主要方法是使用inlineCallbacks 来发送异步请求
        """
        if "location" in item:
            # set by previous step (spider or pipeline). Don't do anything
            # apart from increasing stats
            self.stats.inc_value('geo_pipeline/already_set')
            defer.returnValue(item)
            return

        # The item has to have the address field set
        assert ("address" in item) and (len(item["address"]) > 0)

        # Extract the address from the item
        try:
            item['location'] = yield self.geocode(item["address"][0])
        except:
            self.stats.inc_value('geo_pipelibe/errors')
            print(traceback.format_exc())

        # Return the item for the next stage
        defer.returnValue(item)
