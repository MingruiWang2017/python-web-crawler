import logging

from twisted.internet import defer, protocol, reactor


class CommandSolt(protocol.ProcessProtocol):
    """A ProcessProtocol that sends prices through a binary"""

    def __init__(self, args):
        """初始化成员变量，并启动一个新进程"""
        self._current_deferred = None
        self._queue = []
        reactor.spawnProcess(self, args[0], args)

        self.logger = logging.getLogger('pricing-pipeline')

    def legacy_calculate(self, price):
        """入队一个price来计算"""
        d = defer.Deferred()
        d.addBoth(self._process_done)  # addBoth()方法=addCallback（）和addErrback（）的结合，两者都可以返回
        self._queue.append((price, d))
        self._try_dispatch_top()
        return d

    def _process_done(self, result):
        """当一个计算完成时调用，返回计算值"""
        self._current_deferred = None
        self._try_dispatch_top()
        return result

    def _try_dispatch_top(self):
        """通过发送一个价格到进程中开始一个新的计算"""
        if not self._current_deferred and self._queue:
            price, d = self._queue.pop(0)
            self._current_deferred = d
            self.transport.write("%f\n" % price)

    # 重写protocol.ProcessProtocol的 outReceive方法
    def outReceived(self, data: bytes):
        """called when new output is received"""
        self._current_deferred.callback(float(data))

    def errReceived(self, data: bytes):
        """当发生错误时调用"""
        self.logger.error('PID[%r]: %s' % (self.transport.pid, data.rstrip()))


class Pricing(object):
    """访问legacy功能的管道"""

    @classmethod
    def from_crawler(cls, crawler):
        concurrency = crawler.settings.get('LEGACY_CONCURRENCY', 16)  # 获取并发数
        default_args = ['properties/pipelines/legacy.sh']
        args = crawler.settings.get('LEGACY_ARGS', default_args)  # 获取脚本路径

        return cls(concurrency, args)

    def __init__(self, concurrency, args):
        self.args = args
        self.concurrency = concurrency
        self.slots = [CommandSolt(self.args) for i in range(self.concurrency)]
        self.rr = 0

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        slot = self.slots[self.rr]
        self.rr = (self.rr + 1) % self.concurrency

        item['price'][0] = yield slot.legacy_calculate(item['price'][0])

        defer.returnValue(item)
