import pymysql

# 1. 连接数据库, 连接对象 Connection()
conn = pymysql.Connection(
    host="192.168.73.130",
    port=3306,
    db="school",
    user="spider",
    password="123456"
)
# 2. 创建游标对象 cursor()
cur = conn.cursor()

# 3. 数据操作
# 3.1 查询数据
def query_all():
    """查询表中所有数据"""
    op = "select * from courses"
    count = cur.execute(op)  # execute 命令返回的是数据查询的行数
    result = cur.fetchall()  # fetachall/fetachone 方法获取前一步execut查询到的数据内容
    print(count, ": ", result)
    print("-" * 50)
query_all()

# 3.2 插入数据
op = "insert into courses values(6, 'GO语言')"
result = cur.execute(op)
print(result)

# 提交事务
conn.commit()
query_all()

# 3.3 修改数据
op = "update courses set course='区块链' where id=8"
result = cur.execute(op)
print(result)

# 提交事务
conn.commit()
query_all()

# 3.4 删除数据
op = "delete from courses where id=6"
result = cur.execute(op)
print(result)
# 提交事务
conn.commit()
query_all()

# 4. 关闭游标和连接
cur.close()
conn.close()
