import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

"""计算各个区每平米的平均租价"""

data = pd.read_json('./data/rooms_decode.json', encoding='utf-8')

# 创建df，用于存储均价数据
columns = ["district", "unit_rent"]
rent = pd.DataFrame(columns=columns)

for i in data.index:
    district = data.loc[i]['district']
    unit_rent = data.loc[i]['price'] / data.loc[i]['area']
    other = pd.DataFrame([[district, unit_rent]], columns=columns)
    rent = rent.append(other, ignore_index=True)
print(rent)

# 统计均价
count = rent['district'].value_counts()
print(count)
average_rents = {}

for district in count.keys():
    average_rent = rent[rent["district"]==district].mean()
    average_rents[district] = average_rent['unit_rent']
print(average_rents)

# 绘制水平柱状图
# y_pos = np.arange(len(average_rents))
y_pos = list(average_rents.keys())
y = list(average_rents.values())

plt.barh(y_pos, y, align='center')
plt.yticks(y_pos)
plt.ylabel("地区")
plt.xlabel("平均租价")
plt.title("各地区平均租价")

plt.show()




