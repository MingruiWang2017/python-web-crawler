import traceback
import treq

from twisted.internet import defer, task, reactor

class Throttler(object):
    """
    一个简单的限流器，用来限制每秒发送请求的数量
    """
    def __init__(self, rate):
        """它每秒最多只能调用 rate 个入队的请求"""
        self.queue = []
        # 循环调用_allow_one 方法，该方法是对延迟的回调，实际上就是等待 1/rate s，什么也没干
        self.looping_call = task.LoopingCall(self._allow_one)
        self.looping_call.start(1. / float(rate))   # 延迟时间设置为 1/rate 秒

    def stop(self):
        """停止限流器"""
        self.looping_call.stop()

    def throttle(self):
        """
        Call this function to get a deferred that will become available
        in some point in the future in accordance with the throttling rate
        调用此函数以获取延迟，该延迟将根据节流率在将来的某个时间点变为可用
        """
        d = defer.Deferred()
        self.queue.append(d)
        return d

    def _allow_one(self):
        """周期性地进行延迟回调"""
        if self.queue:
            # 实际上queue中的延时没有回调函数，其callback就是直接返回None
            self.queue.pop(0).callback(None)


class DeferredCache(object):
    """
    因为我们查询的地理位置有限，为了防止反复向服务器发送请求，为其设置一个缓存
    之前已经查询到的地理编码会直接返回，没有查询过的再发送请求查询
    该缓存可能返回一个值（之前已经缓存的结果）、一个错误（接口无法查到）或者一个延时(之前未查询过的新地址，发送请求)
    """
    def __init__(self, key_not_found_callback):
        self.records = {}  # 已查询结果的记录---缓存
        self.deferreds_waiting = {}  # 一个延时操作的队列，等待指定键的值
        self.key_not_found_callback = key_not_found_callback

    @defer.inlineCallbacks
    def find(self, key):
        """
        这个方法可能从缓存中直接返回一个值，
        或者调用 key_not_found_callback 方法来查询值并返回。
        使用延迟来进行该操作，实现非阻塞
        """
        # 为方法创建用于调用的延时
        rv = defer.Deferred()

        if key in self.deferreds_waiting:
            # we have other instances waiting for this key. Queue
            # 如果新来的key查询，还在等待查询的队列中，则添加这个新的查询到队列中，等待
            self.deferreds_waiting[key].append(rv)
        else:
            # we are the only guy waiting for this key right now
            # 如果先来的key查询，没在等待查询的队列中，则为这个key创建一个新队列
            self.deferreds_waiting[key] = [rv]

            if not key in self.records:
                # if we don't have a value for this key, we will evaluate it
                # using key_not_found_callback
                # 如果records中没有该key的记录，则回调查询api进行查询
                try:
                    value = yield self.key_not_found_callback(key)

                    # if the evaluation succeeds then the action for this key
                    # is to call deferred's callback with value as an argument
                    # (using python closures)
                    # 如果查询成功,records中保存的是一个lambda函数，函数参数是延时d，调用的话则返回value，使用的是python闭包（closure）
                    self.records[key] = lambda d: d.callback(value)
                except Exception as e:
                    # if the evaluation fails with an exception then the
                    # action for this key is to call deferred's errback with
                    # the exception as an argument(python closures again)
                    # 如果查询失败，key对应保存的是一个lambda函数，函数参数是延时d，调用的话则返回异常信息
                    self.records[key] = lambda d: d.errback(e)

            # at this point we have an action for this key in self.recodes
            # 如果要查询的key在records中，则获取之前保存的回调方法
            action = self.records[key]

            # Note: due to ```yield key_not_found_callback```, many
            # deferreds might have been added in deferreds_waiting[key] in
            # the meanwhile
            # for each of the deferreds_waitng for this key ...
            for d in self.deferreds_waiting.pop(key):
                # ...perform the action later from the reactor thread
                reactor.callFromThread(action, d)  # 执行action(d)，返回之前保存的查询结果或异常

        value = yield rv
        defer.returnValue(value)


class GeoPipeline(object):
    """用于转换地理编码的管道"""
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def __init__(self, stats):
        self.stats = stats
        self.cache = DeferredCache(self.cache_key_not_found_callback) # 添加缓存
        self.throttler = Throttler(5)  # 设置限流器，限制每秒5个请求

    def close_spider(self, spider):
        """爬虫关闭时，关闭限流器"""
        self.throttler.stop()

    @defer.inlineCallbacks
    def geocode(self, address):
        endpoint = "http://192.168.73.130:9312/maps/api/geocode/json"

        # 发送请求
        params = [('address', address), ('sensor', 'false')]
        response = yield treq.get(endpoint, params=params)

        # 解析响应
        content = yield response.json()
        if content['status'] != "OK":
            raise Exception("Unexpected status=\"%s\" for address=\"%s\"" %
                            (content['status'], address))

        # 得到地理编码
        geo = content['results'][0]["geometry"]["location"]
        defer.returnValue({"lat": geo["lat"], "lon": geo["lng"]})


    @defer.inlineCallbacks
    def cache_key_not_found_callback(self, address):
        """
        此方法在遵守限制的同时进行API调用。它还会重试由于限制而失败的尝试。
        """
        self.stats.inc_value('geo_pipeline/misses')  # 在日志的统计信息中添加统计项，每调用一次该项加1

        while True:
            # 等待足够多的时间来坚持节流政策
            yield self.throttler.throttle()

            # 调用API
            try:
                value = yield self.geocode(address)
                defer.returnValue(value)

                # success
                break
            except Exception as e:
                if 'status="OVER_QUERY_LIMIT"' in str(e):
                    # 如果查询保存超出请求限制，重试
                    self.stats.inc_value("geo_pipeline/retrties")
                    continue
                # 其他情况将异常继续抛出
                raise

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        """向ES发送请求保存数据"""
        if "location" in item:
            self.stats.inc_value('geo_pipeline/already_set')
            defer.returnValue(item)
            return

        # 确保item包含address字段
        assert ("address" in item) and (len(item["address"]) > 0)

        try:
            item['location'] = yield self.cache.find(item["address"][0])
        except:
            self.stats.inc_value("geo_pipeline/errors")
            print(traceback.format_exc())

        defer.returnValue(item)
