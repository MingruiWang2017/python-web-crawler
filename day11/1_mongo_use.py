import pymongo
from urllib.parse import quote_plus

# 1. 连接数据库服务
host = "192.168.73.130"
username = "A"
password = "123456"
# 1.1 使用参数连接
# 不指定用户登录
# client = pymongo.MongoClient(host, 27017)
# 使用用户信息登录
# client = pymongo.MongoClient(host, 27017, username=username, password=password)

# 1.2 使用 uri 连接, ref: https://docs.mongodb.com/manual/reference/connection-string/
# mongodb+srv://<username>:<password>@<cluster-address>/test?retryWrites=true&w=majority
conn_str = "mongodb://%s:%s@%s/?retryWrites=true&w=majority" % (
    quote_plus(username), quote_plus(password), host
)
print(conn_str)
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)

# 2. 库
db = client['one']
# db = client.one

# 3. 集合
# col = db.teacher
# col = db['teacher']
# col = client.one.teacher
col = client['one']['teacher']


# 4. 操作数据
try:
    # 1. 查看数据
    result = col.find_one({"name": "王五"})
    print(result)
    print("-" * 80)

    for doc in col.find():
        print(doc)
    print("-" * 80)

    # 2.单个插入数据
    data1 = {"name": "Jerry", "age": 27, "salary": 8989.90, "gender": "male"}
    # col.insert_one(data1)

    # 3. 批量插入数据
    data2 = [
        {"name": "李四", "age": 27, "salary": 8989.90, "gender": "male"},
        {"name": "Jerry3", "age": 27, "salary": 9089.90, "gender": "male"},
        {"name": "Jerry3", "age": 47, "salary": 7089.90, "gender": "male"},
        {"name": "Jerry4", "age": 37, "salary": 9889.90, "gender": "male"},
        {"name": "Jerry5", "age": 57, "salary": 8789.90, "gender": "male"},
    ]
    col.insert_many(data2)

    print("-" * 80)
    for doc in col.find():
        print(doc)

    # 4. 删除数据
    col.delete_one({"age": 37})
    print("-" * 80)
    for doc in col.find():
        print(doc)

    col.delete_many({"age": {"$gt": 37}})
    print("-" * 80)
    for doc in col.find():
        print(doc)

    # 5.修改数据
    # replace 将目标替换为新的文档
    col.replace_one({"name": "李四"}, {"name": "李老四", 'age': 31.0, 'salary': 8888.88})

    # udapte 在修改时需要使用 $set、$inc 等动词
    col.update_one({"name": "张三"}, {"$set": {"age": "34"}})
    print("-" * 80)
    for doc in col.find():
        print(doc)

    col.update_many({"age": 22}, {'$inc': {'salary': 300}})
    print("-" * 80)
    for doc in col.find():
        print(doc)

    # 6.查看索引
    print("=" * 80)
    indexes = col.index_information()
    print(indexes)
    # 7. 添加索引
    col.create_index("age")
    indexes = col.index_information()
    print(indexes)
    # 8. 删除索引
    col.drop_index("age_1")
    indexes = col.index_information()
    print(indexes)

except Exception as e:
    print(e)
finally:
    client.close()
