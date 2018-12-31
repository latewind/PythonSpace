import numpy as np
import pandas as pd

data = {'name': ['Tomcat', 'eclipse', 'idea'],
        'download': [100, 200, 300],
        'price': [0.0, 1.0, 500]}

df = pd.DataFrame(data, index=['a', 'b', 'c'])
print(df)

# reindex 不改变原来的结构，返回一个新的
df2 = df.reindex(['a', 'b', 'c', 'd'])
print(df2)

df3 = df.reindex(columns=['name', 'download', 'price', 'VS'])
print(df3)

# 删除行
df4 = df.drop(['a', 'c'])
print(df4)
# 删除列
df5 = df.drop(['name'], axis=1)
print(df5)
# 原数据上做修改
df.drop(['c'], inplace=True)
print(df)

print(df < 5)

sel = df.loc['a', ['name', 'price']]
print(sel)
isel = df.iloc[[0], [0, 1]]
print(isel)
