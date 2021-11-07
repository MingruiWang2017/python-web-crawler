import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

data = pd.read_json('./data/rooms_decode.json')

# 计算每平米的单位租金
unit_rent = []
for i in range(len(data)):
    # print(data.iloc[i]['price'], data.iloc[i]['area'])
    unit_rent.append(data.iloc[i]['price'] / data.iloc[i]['area'])

unit_rent_values = np.array(unit_rent)

# 绘制柱状图
plt.hist(unit_rent_values, bins=50)
plt.xlim(unit_rent_values.min()-1, unit_rent_values.max()+1)
plt.title("平均每平出租价格")
plt.xlabel("价格（元/平米）")
plt.ylabel('数量')
plt.show()