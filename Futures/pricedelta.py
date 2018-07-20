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
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.ticker as ticker
from matplotlib.ticker import Formatter, FixedLocator

"""
沪铜1809 和 沪锌1809 价格差
"""

column_index = ['名称', '位置', '开盘价', '最高价', '最低价', '昨日收盘价', '买价', '卖价', '最新价', '结算价', '昨结算', '买量', '卖量', '持仓量', '成交量']
# 沪铜1809数据接口和格式
CU1809_URL = "http://hq.sinajs.cn/?_=0/&list=CU1809"
CU1809_STRIP_STR = 'varhq_str_CU1809=" ;\n'
# 数据格式

# 沪铜1809数据接口和格式
ZN1809_URL = "http://hq.sinajs.cn/?_=0/&list=ZN1809"
ZN1809_STRIP_STR = 'varhq_str_ZN1809=" ;\n'
# 数据格式

data_type = {i: 'float' for i in range(3, 11)}

# 主题黑色
plt.style.use('dark_background')

# ax = host_subplot(111)
fig, ax = plt.subplots()
plt.subplots_adjust(left=.09, bottom=.14, right=.94, top=.95, wspace=.20, hspace=0)
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置
# plt.rcParams['axes.unicode_minus'] = False
plt.title(u"CU1809  -  ZN1809")


def on_move(event):
    # get the x and y pixel coords
    x, y = event.x, event.y

    if event.inaxes:
        ax = event.inaxes  # the axes instance
        # print('data coords %f %f' % (event.xdata, event.ydata))
        # print(num2date(event.xdata))


plt.connect('motion_notify_event', on_move)


# plt.axis([0, 1, 86400, 1.0 *50000])

def fetch_futures_data(url, strip_str):
    ctx = requests.get(url)
    data = [datetime.datetime.now()] + ctx.text.strip(strip_str).split(",")
    dt = pd.DataFrame([data])  # dtype='float
    dt = dt.astype(dtype=data_type)  # 类型转换
    return dt


def fetch_futures_data_light(url, strip_str):
    ctx = requests.get(url)
    new_price = ctx.text.strip(strip_str).split(",")[8]
    return float(new_price)


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


def convert_date(t):
    def convert_float_to_int(y):
        return int(np.round(y))

    if t_slot[0][0] <= t <= t_slot[0][1]:
        return convert_float_to_int(t.timestamp() - t_slot[0][0].timestamp() + time_interval[0][0])

    if t_slot[1][0] <= t <= t_slot[1][1]:
        return convert_float_to_int(t.timestamp() - t_slot[1][0].timestamp() + time_interval[1][0])

    if t_slot[2][0] <= t <= t_slot[2][1]:
        return convert_float_to_int(t.timestamp() - t_slot[2][0].timestamp() + time_interval[2][0])

    if t_slot[3][0] <= t <= t_slot[3][1]:
        return convert_float_to_int(t.timestamp() - t_slot[3][0].timestamp() + time_interval[3][0])
    return False


class Futures:
    def __init__(self):
        init_time()
        self.today = datetime.date.today()
        self.today.timetuple()
        self.today_start_time = int(time.mktime(time.strptime(str(self.today), '%Y-%m-%d')))

        self.start_date = datetime.datetime.fromtimestamp(self.today_start_time)
        self.end_date = self.start_date + datetime.timedelta(hours=24)
        self.delta = datetime.timedelta(minutes=1)
        dates = drange(self.start_date, self.end_date, self.delta)

        self.prices = []
        self.times = []
        # DataFrame
        self.cu_data = pd.DataFrame([])

        self.Y_MAX_NUM = 1
        self.Y_MIN_NUM = 0

        self.random = random.Random()

        self.line, = ax.plot(self.times, self.prices, '-')
        # self.line ,= ax.plot(self.times, self.prices, '-')
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        ax.xaxis.set_major_locator(FixedLocator(time_dims))

        ax.set_xlim(0, 27900)

        ax.grid(color='w', linestyle='-', linewidth=.2)
        fig.autofmt_xdate()
        pass

    def _fetch_data(self):
        cur_time = time.time()
        cur_time_sec = int(round(cur_time))
        time_dlt = int(cur_time - self.today_start_time)

        t = int(round(cur_time * 1000))
        # 获取数据 处理
        ctx = requests.get(CU1809_URL)
        data = [datetime.datetime.now()] + ctx.text.strip('varhq_str_CU1809=" ;\n').split(",")

        dt = pd.DataFrame([data])  # dtype='float
        dt = dt.astype(dtype={9: "float"})  # 类型转换
        self.cu_data = pd.concat([self.cu_data, dt], ignore_index=True)  # 合并数据

        #
        price = self._gen_C1809_price()
        self.prices.append(price)
        self.times.append(datetime.datetime.now())
        # print(float(price))

        if price > self.Y_MAX_NUM:
            self.Y_MAX_NUM = price * 1.001
        if price < self.Y_MIN_NUM:
            self.Y_MIN_NUM = price * 0.999

    def _fetch_cu1809_price(self):
        # return float(self.random.randint(48000, 50000))
        current_price = fetch_futures_data_light(CU1809_URL, CU1809_STRIP_STR)
        return float(current_price)

    def _fetch_zn1809_price(self):
        # return float(self.random.randint(48000, 50000))
        current_price = fetch_futures_data_light(ZN1809_URL, ZN1809_STRIP_STR)
        return float(current_price)

    def _update_ylim(self):
        new_y_min_num = self.prices[-1] - 100.0  # 最低价
        new_y_max_num = self.prices[-1] + 100.0  # 最高价
        if self.Y_MAX_NUM == 1 and self.Y_MIN_NUM == 0:
            self.Y_MIN_NUM, self.Y_MAX_NUM = new_y_min_num, new_y_max_num
            ax.set_ylim((self.Y_MIN_NUM, self.Y_MAX_NUM))

        if new_y_max_num > self.Y_MAX_NUM:
            self.Y_MAX_NUM = new_y_max_num
            ax.set_ylim((self.Y_MIN_NUM, self.Y_MAX_NUM))

        if new_y_min_num < self.Y_MIN_NUM:
            self.Y_MIN_NUM = new_y_min_num
            ax.set_ylim((self.Y_MIN_NUM, self.Y_MAX_NUM))

    def on_timer(self):
        # time.sleep(3)
        cu_cur_price = self._fetch_cu1809_price()
        zn_cur_price = self._fetch_zn1809_price()
        price_delta = cu_cur_price - zn_cur_price
        print(cu_cur_price, zn_cur_price, price_delta)
        # price_delta = random.randrange()
        t_delta = convert_date(datetime.datetime.now())
        if t_delta is not False:
            self.prices.append(price_delta)
            self.times.append(t_delta)

        # self.range_s += self.range_step
        # self.range_e += self.range_step
        # t = np.arange(self.range_s, self.range_e, self.range_step)
        # ydata = np.sin(4 * np.pi * t)
        # 更新数据
        # x.plot(self.times, self.prices)
        # print(self.cu_data.dtypes)

        # self.line.set_ydata(self.prices)
        # 更新数据
        # print(self.prices)
        self.line.set_xdata(self.times)
        self.line.set_ydata(self.prices)
        # print(self.cu_data.tail(1)[4])
        self._update_ylim()

        # print(self.cu_data[0].values)
        # print(self.cu_data[9].tolist())

        # 更新坐标
        # ax.set_ylim((self.Y_MIN_NUM, self.Y_MAX_NUM))
        # 重新绘制图形
        ax.figure.canvas.draw()
        fig.canvas.flush_events()
        # plt.draw()


if __name__ == '__main__':
    f = Futures()
    # f.start()
    # # plt.subplots_adjust(left=.09, bottom=.14, right=.94, top=.95, wspace=.20, hspace=0)
    timer = fig.canvas.new_timer(interval=3000)
    timer.add_callback(f.on_timer)
    timer.start()

    cursor = Cursor(ax, useblit=True, color='w', linestyle='--', linewidth=.5)

    plt.show()

"""
s= ax.transData.transform((0, 0))
print(tuple(s))
s= tuple(s)
ax.annotate('figure points',
            xy=s, xycoords='figure points')
ax.annotate('figure fraction',
            xy=(.025, .975), xycoords='figure fraction',
            horizontalalignment='left', verticalalignment='top',
            fontsize=20)

"""
