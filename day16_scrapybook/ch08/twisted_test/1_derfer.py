from twisted.internet import defer

# 延时
d = defer.Deferred()

print(d.called)

# 调用
d.callback(3)

print(d.called)

# 结果
print(d.result)