from twisted.internet import defer, task, reactor

"""限制并发数量
对于4中的协程，如果客户的数量是10000个，name他会同时开启10000个处理序列（如HHTP请求，数据库写操作等），
这可能会导致一些问题和失败。
在大规模并发应用中，一般需要限制并发量在可以接受的水平。
使用task.Cooperator() 来限制并发数量。
"""

@defer.inlineCallbacks
def inline_install(customer):
    print("Scheduleing: Installation for ", customer)
    yield task.deferLater(reactor, 3, lambda : None)
    print("Callback: Finished installation for ", customer)
    print("All done for ", customer)


def twisted_develop_day(customers):
    print("Good morning from twisted developer")
    work = (inline_install(customer) for customer in customers) # 改为元组

    # 设置并发数为5
    coop = task.Cooperator()
    join = defer.DeferredList([coop.coiterate(work)
                               for _ in range(5)])
    join.addCallback(lambda _: reactor.stop())

    print("Bye from Twisted developer!")

twisted_develop_day(["Customer %d" % i for i in range(15)])

reactor.run()

# 15个顾客，每次并发处理5个，共耗时9秒