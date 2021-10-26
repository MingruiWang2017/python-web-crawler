import redis

# 1. 连接数据库
host = "192.168.73.130"
port = 6379
password = "123456"

# 1.1 使用参数连接
# 查询结果是bytes类型，设置decode_responses=True将结果解码为str
# client = redis.StrictRedis(host=host, port=port, db=1,
#                            password=password, decode_responses=True)
# 1.2 使用uri连接
# conn_str = "redis://:{}@{}:{}/2".format(password, host, port)
# client = redis.from_url(url=conn_str, decode_responses=True)
# 1.3 使用连接池
pool = redis.ConnectionPool(host=host, port=port, db=2, password=password, decode_responses=True)
client = redis.StrictRedis(connection_pool=pool)

# 2. 设置 key
key = "pyone"

# 3. string操作
# 3.1 增
result = client.set(key, "1")
print(result)
# 3.2 删
result = client.delete(key)
print(result)

# 3.3 改
result = client.set(key, "1")
print(result)
result = client.set(key, "one")
print(result)

# 3.4 查
result = client.get(key)
print(result)

# 4. 查询keys
keys = client.keys('*')
print(keys)

# 5. 关闭连接
client.close()