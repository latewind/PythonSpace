import pandas as pd
import numpy as np

data = {'name': ['Tomcat', 'eclipse', 'idea'],
        'download': [100, 200, 300],
        'price': [0.0, 1.0, 500]}

df = pd.DataFrame(data)
print(df)

# 指定列顺序
df = pd.DataFrame(data, columns=['price', 'download', 'name'])
print(df)

# 指定列顺序
data['status'] = ['open', 'close', 'open']
df = pd.DataFrame(data)

df.index = ['one', 'two', 'three']

# 获取列的值
df['price']
df.download

# 给列赋值
df['price'] = 100
print(df)

df['price'] = np.arange(3.0)
print(df)

# 获取某一列
frame = df.loc['one']
print(frame)

# 转置
print(df.T)

df.index.name = 'index'
print(df)

df.reindex()

