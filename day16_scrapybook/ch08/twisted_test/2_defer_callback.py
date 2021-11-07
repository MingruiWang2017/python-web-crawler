from twisted.internet import defer

d = defer.Deferred()


def foo(v):
    print("foo called")
    return v + 1


# 添加回调方法
d.addCallback(foo)
print(d.called)

# 调用回调方法并传参v=3
d.callback(3)
print(d.called)

print(d.result)
