import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

"""绘制饼图，查看不同租房类型下各个地区房源数量"""

# 为matplotlib设置显示字体, 将全局字体设为简黑
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(10, 30))

# 1. 导入数据
data = pd.read_json('./data/rooms_decode.json', encoding='utf-8')
data = pd.DataFrame(data)
# print(data)

# 2. 统计不同租房类的数量
rent_type = data['rent_type'].value_counts()

# 3. 获取不同市区的租房数量信息
district_count = data['district'].value_counts()

labels = "钱塘", "萧山", "临平", "拱墅", "西湖", "余杭", "临安", "上城", "滨江", "建德", "富阳"

sizes = dict(district_count).values()
explode = (0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
plt.subplot(131)

# 4. 所有房源不同地区统计图
plt.pie(sizes, explode=explode, labels=labels,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.title('各地区房源数量汇总')

# 5. 整租房源不同地区统计图
zhengzu_data = data[data["rent_type"] == "整租"]
zhengzu_count = zhengzu_data['district'].value_counts()

labels = dict(zhengzu_count).keys()
sizes = dict(zhengzu_count).values()

plt.subplot(132)
plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.title("整租房源各地区数量汇总")

# 6. 合租房源不同地区统计图
hezu_data = data[data["rent_type"] == "合租"]
hezu_count = hezu_data['district'].value_counts()

labels = dict(hezu_count).keys()
sizes = dict(hezu_count).values()

plt.subplot(1, 3, 3)
plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.title("合租房源各地区数量汇总")

plt.show()
