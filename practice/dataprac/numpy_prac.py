import numpy as np

a = np.arange(10., 20)
obj = a[[1, 2, 5]]
print(obj)

obj = a[2:7:2]
print(obj)

obj = a[4]
print(obj)

b = np.arange(0, 12).reshape(3, 4)
print(b)

obj = b[1:, [1, 2]]
print(obj)

obj = b[b > 5]
print(obj)

print("#" * 10)
obj = b[np.ix_([2, 1, 0], [0, 2, 1])]
print(obj)

names = np.array(['A', 'B', 'C', 'D', 'B'])
data = np.random.randn(5, 2)
print(data)
print(data[names == 'B'])
print(data[~(names == 'B')])
print(data[[True, False, False, False, False]])
