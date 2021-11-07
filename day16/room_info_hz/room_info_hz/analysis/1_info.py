import pandas as pd

"""使用pandas查看爬取的租房信息基本数据"""

# 读取信息
df = pd.read_json('./data/rooms.json')
df = pd.DataFrame(df)  # 可以不添加类型转换，添加后编辑器可以自动联想方法
print("数据内容: ".center(100, "="), "\n", df)

# 查看数据字段名称
print("数据字段：".center(100, "="), "\n", df.columns)

# 查看数据基本描述
print("description".center(50, "="), "\n", df.describe())

# 按照字段，统计字段中各类的数量
print("租房类型统计".center(50, "="), "\n", df["rent_type"].value_counts())



