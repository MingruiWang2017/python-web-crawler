import time
import threading

from twisted.internet import reactor, defer

"""处理CPU密集型或阻塞操作的管道：使用reactor.callInThread()和reactor.callFromThread()
将阻塞操作放在其他线程中执行，如果存在全局状态值，需要对其使用线程锁"""


class UsingBlocking(object):
    """A pipeline that fakes some computation or blocking calls"""

    def __init__(self):
        """
        This function doesn't need any settings so init just initializes a few
        fields
        """
        # 全局状态量
        self.beta, self.delta = 0, 0
        self.lock = threading.RLock()  # 线程递归锁

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        """将回调阻塞操作的延迟放到twisted reactor的线程池中"""

        # get the price
        price = item['price'][0]

        # 在线程池中调用一个复杂或者阻塞的方法
        # 注意：这虽然讲给你带来一些性能上的提升，但它依然受限于GIL，
        # 很可能无法充分利用多核CPU/cores 的系统。
        # 可以考虑Twisted的 spawnProcess() 方法或者
        # 围绕python的multiprocessing.Process制作一个自定义的解决方案，
        # 以充分利用你的核心来完成CPU密集型任务。
        # 也可以考虑把这个处理作为一个批处理的后处理步骤。
        out = defer.Deferred()
        reactor.callInThread(self._do_calculation, price, out)

        # yield 等待结果并作为新的price值
        item['price'][0] = yield out

        # 返回item共其他阶段的管道使用
        defer.returnValue(item)

    def _do_calculation(self, price, out):
        """
        只是一个缓慢的计算。注意，该方法使用锁来保护全局状态量。
        如果你不适用锁同时又有全局状态用，那么将会得到错误的数据
        """
        # 使用锁来保护关键部分
        with self.lock:
            # 使用全局状态量伪造一个复杂的计算
            self.beta += 1
            # 尽可能少的时间来持有锁。这里通过sleep 1 ms 使数据在你没有持有锁的情况下更有可能损坏
            time.sleep(0.001)
            self.delta += 1
            new_price = price + self.beta - self.delta + 1  # = price + 1

        # 使用断言确保经过“复杂”计算后，最终结果必须保持正确
        assert abs(new_price - price - 1) < 0.01, "%f != %f" % (new_price, price)

        # 执行某些不需要全局状态量的计算
        time.sleep(0.1)

        # 将处理过程放入reactor的主线程队列
        reactor.callFromThread(out.callback, new_price)
