import time
from twisted.internet import defer, task, reactor

"""使用twisted异步IO"""


def schedule_install(customer):
    def schedule_install_wordpress():
        def on_done():
            print("Callback: Finished installation for", customer)

        print("Scheduling: Installation for", customer)
        return task.deferLater(reactor, 3, on_done)  # 使用该方法告诉事件反应器，等待3秒后在执行回调函数

    def all_done(_):
        print("All done for", customer)

    d = schedule_install_wordpress()
    d.addCallback(all_done)

    return d


def twisted_developer_day(customers):
    print("Good morning from twisted developer")
    work = [schedule_install(customer) for customer in customers]

    join = defer.DeferredList(work)
    join.addCallback(lambda _: reactor.stop())

    print("Bye from Twisted developer!")


start_time = time.time()
twisted_developer_day(["Customer %d" % i for i in range(15)])

reactor.run()  # 代码的实际执行

used_time = time.time() - start_time
print("The func used %f seconds" % used_time)

# 使用异步IO，当遇到阻塞时，就切换到其他非阻塞的地方继续执行
# 共耗时3秒
