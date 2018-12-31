import pandas as pd


def foo():
    obj = 123


obj = pd.Series([1, 2, 3, 4])

obj = pd.Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'])

obj.index

obj.values

sdata = {'red': 100, 'blue': 200, 'green': 300}
obj = pd.Series(sdata)

obj[obj < 2]

obj = pd.Series(sdata, ['red', 'blue', 'green', 'yellow'])




