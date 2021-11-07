from twisted.internet import defer


def on_done(arg):
    print("on_done called with arg = ", arg)
    return arg


deferreds = [defer.Deferred() for i in range(5)]

# 延迟链
join = defer.DeferredList(deferreds)
join.addCallback(on_done)

for i in range(4):
    deferreds[i].callback(i)

print(deferreds[3].result)

print("=" * 30)

deferreds[4].callback(4)

# 由结果
# on_done called with arg =  [(True, 0), (True, 1), (True, 2), (True, 3), (True, 4)]
# 可知，虽然前4个延迟以及被调用了，但是最后on_done()仍需要等到列表中所有延迟都被触发才会调用
# on_done 的参数是一个元组组成的列表，每个元组对应一个延迟，其中包含两个元素，
# 分别是表示成功的True或失败的False，和延迟的result
