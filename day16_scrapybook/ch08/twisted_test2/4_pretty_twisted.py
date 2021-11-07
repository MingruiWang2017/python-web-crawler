from twisted.internet import defer, task, reactor

"""使用twisted的装饰器来简化3中的代码
inlineCallbacks 生成器使用了一些Python机制让inline_install() 的代码能够暂停和恢复。
inline_install() 变为延迟函数，并且为每位客户并行执行。
每当执行yield 时，执行会在当前的inline_install() 实例上暂停，当yield的延迟函数触发时再恢复。
"""

@defer.inlineCallbacks
def inline_install(customer):
    print("Scheduleing: Installation for ", customer)
    yield task.deferLater(reactor, 3, lambda : None)
    print("Callback: Finished installation for ", customer)
    print("All done for ", customer)


def twisted_develop_day(customers):
    print("Good morning from twisted developer")
    work = [inline_install(customer) for customer in customers]

    join = defer.DeferredList(work)
    join.addCallback(lambda _: reactor.stop())

    print("Bye from Twisted developer!")

twisted_develop_day(["Customer %d" % i for i in range(15)])

reactor.run()