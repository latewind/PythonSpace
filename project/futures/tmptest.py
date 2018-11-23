import matplotlib.ticker as ticker
import time
import requests
import matplotlib.pyplot as plt
from threading import Thread
import datetime
import random
import numpy as np
import pandas as pd
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, num2date
from matplotlib.widgets import Cursor
from matplotlib.ticker import Formatter, FixedLocator

# Fixing random state for reproducibility
np.random.seed(19680801)

fig, ax = plt.subplots()
# ax.plot(100*np.random.rand(20))

t = [None for _ in range(0, 8)]
t_slot = [(None, None) for _ in range(0, 4)]

# 各个时间间隔
time_interval = [(0, 14399), (14400, 18899), (18900, 22499), (22500, 27900)]
# 坐标轴刻度
time_dims = [0, 14400, 18900, 22500, 27900]


def init_time():
    today = datetime.datetime.today()
    cur_hour = today.hour
    t0 = None
    # 晚上21:00 之前 ，起点是昨日的21:00
    if cur_hour < 21:
        t0 = datetime.datetime.combine(today.date() - datetime.timedelta(hours=24), datetime.time(21, 0, 0))
    else:
        t0 = datetime.datetime.combine(today.date(), datetime.time(21, 0, 0))
    t1 = t0 + datetime.timedelta(hours=4) - datetime.timedelta(seconds=1)  # 1:00
    t_slot[0] = (t0, t1)

    t2 = t0 + datetime.timedelta(hours=12)  # 9:00
    t3 = t0 + datetime.timedelta(hours=13, minutes=15) - datetime.timedelta(seconds=1)  # 10:15
    t_slot[1] = (t2, t3)

    t4 = t0 + datetime.timedelta(hours=13, minutes=30)  # 10:30
    t5 = t0 + datetime.timedelta(hours=14, minutes=30) - datetime.timedelta(seconds=1)  # 11:30
    t_slot[2] = (t4, t5)

    t6 = t0 + datetime.timedelta(hours=16, minutes=30)  # 13:30
    t7 = t0 + datetime.timedelta(hours=18)  # 15:00
    t_slot[3] = (t6, t7)

    [print(t_slot[_]) for _ in range(0, len(t_slot))]


init_time()

"""
用着总方式来格式坐标轴
"""


def format_date(x, pos=None):
    x = int(x)
    if time_interval[0][0] <= x <= time_interval[0][1]:
        return (t_slot[0][0] + datetime.timedelta(seconds=x)).time()

    if time_interval[1][0] <= x <= time_interval[1][1]:
        return (t_slot[1][0] + datetime.timedelta(seconds=(x - time_interval[1][0]))).time()

    if time_interval[2][0] <= x <= time_interval[2][1]:
        return (t_slot[2][0] + datetime.timedelta(seconds=(x - time_interval[2][0]))).time()

    if time_interval[3][0] <= x <= time_interval[3][1]:
        return (t_slot[3][0] + datetime.timedelta(seconds=(x - time_interval[3][0]))).time()

    return x


ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
ax.xaxis.set_major_locator(FixedLocator(time_dims))

ax.set_xlim(0, 27900)

for tick in ax.yaxis.get_major_ticks():
    tick.label1On = True
    tick.label2On = True
    tick.label2.set_color('green')

plt.show()
