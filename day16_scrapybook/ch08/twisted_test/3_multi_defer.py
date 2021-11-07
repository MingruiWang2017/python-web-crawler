from twisted.internet import defer


def status(*ds):  # *ds 可以在调用时将多个参数，转换为元组使用
    """查看延迟的结果和待被调用的方法数量"""
    return [(getattr(d, 'result', 'N/A'), len(d.callbacks))
            for d in ds]


def b_callback(arg):
    print("b_callback called with arg = ", arg)
    return b  # b是一个defer


def on_done(arg):
    print("on_done called with arg = ", arg)
    return arg


# 使用两个延迟
a = defer.Deferred()
b = defer.Deferred()
a.addCallback(b_callback).addCallback(on_done)

print(status(a, b))

a.callback(3)
# 此时调用了b_callback方法，返回值时b，相当于此时的
# a.addCallback(b_callback).addCallback(on_done) = b.addCallback(on_done)

# 现在b 也包含了一个回调。实际上是在后台注册了一个回调，一旦触发b ，就会更新它的值。

print(status(a, b))

b.callback(4)

print(status(a, b))
# 虽然是b调用了on_done方法，但是result为None，4返回给了a

#################################################################################
print("交换顺序执行".center(80, "="))


def d_callback(arg):
    print("d_callback called with arg = ", arg)
    return d


c = defer.Deferred()
d = defer.Deferred()

c.addCallback(d_callback).addCallback(on_done)
print(status(c, d))

# d先回调
d.callback(4)
print(status(c, d))

c.callback(3)

print(status(c, d))

# 交换顺序后最终结果是一样的，也就是说，动作在阻塞是可能执行顺序是不同的，但最后的结果是幂等的
