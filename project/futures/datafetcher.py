import time
import requests
import matplotlib.pyplot as plt
from threading import Thread
import datetime
import random
import numpy as np
import pandas as pd
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange,num2date
from matplotlib.widgets import Cursor

from mpl_toolkits.axes_grid1 import host_subplot

column_index = ['名称', '位置', '开盘价', '最高价', '最低价', '昨日收盘价', '买价', '卖价', '最新价', '结算价', '昨结算', '买量', '卖量', '持仓量', '成交量']
# 沪铜1809数据接口和格式
CU1809_URL = "http://hq.sinajs.cn/?_=0/&list=CU1809"
CU1809_STRIP_STR = 'varhq_str_CU1809=" ;\n'
# 数据格式
data_type = {i: 'float' for i in range(3, 11)}

# 主题黑色
plt.style.use('dark_background')

# ax = host_subplot(111)
fig, ax = plt.subplots()
plt.subplots_adjust(left=.09, bottom=.14, right=.94, top=.95, wspace=.20, hspace=0)

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


class Futures:
    def __init__(self):
        self.today = datetime.date.today()
        self.today_start_time = int(time.mktime(time.strptime(str(self.today), '%Y-%m-%d')))

        self.start_date = datetime.datetime.fromtimestamp(self.today_start_time)
        self.end_date = self.start_date + datetime.timedelta(hours=24)
        self.delta = datetime.timedelta(minutes=1)
        dates = drange(self.start_date, self.end_date, self.delta)

        y = np.arange(len(dates))

        self.prices = []
        self.times = []
        # DataFrame
        self.cu_data = pd.DataFrame([])

        self.Y_MAX_NUM = 48999
        self.Y_MIN_NUM = 48000

        self.random = random.Random()

        self.line, = ax.plot(self.times, self.prices, '-')
        # self.line ,= ax.plot(self.times, self.prices, '-')
        ax.set_xlim(self.start_date, self.end_date)
        ax.xaxis.set_minor_locator(HourLocator(range(0, 25, 6)))
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

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

    def _fetch_c1809_data(self):
        # return float(self.random.randint(48000, 50000))
        new_data = fetch_futures_data(CU1809_URL, CU1809_STRIP_STR)
        self.cu_data = pd.concat([self.cu_data, new_data], ignore_index=True)  # 合并数据

    def _update_ylim(self):
        new_y_min_num = float(self.cu_data.tail(1)[5]) - 100.0  # 最低价
        new_y_max_num = float(self.cu_data.tail(1)[4]) + 100.0  # 最高价
        if new_y_max_num != self.Y_MAX_NUM or new_y_min_num != self.Y_MIN_NUM:
            print(new_y_min_num, new_y_max_num)
            print(self.Y_MIN_NUM, self.Y_MAX_NUM)
            self.Y_MIN_NUM, self.Y_MAX_NUM = new_y_min_num, new_y_max_num
            ax.set_ylim((self.Y_MIN_NUM, self.Y_MAX_NUM))

    def on_timer(self):
        # print("on_timer invoke begin")
        # time.sleep(3)
        self._fetch_c1809_data()
        # self.range_s += self.range_step
        # self.range_e += self.range_step
        # t = np.arange(self.range_s, self.range_e, self.range_step)
        # ydata = np.sin(4 * np.pi * t)
        # 更新数据
        # x.plot(self.times, self.prices)
        # print(self.cu_data.dtypes)

        # self.line.set_ydata(self.prices)
        # 更新数据
        self.line.set_xdata(self.cu_data[0].values)
        self.line.set_ydata(self.cu_data[9].tolist())
        # print(self.cu_data.tail(1)[4])
        self._update_ylim()

        # print(self.cu_data[0].values)
        # print(self.cu_data[9].tolist())

        # 更新坐标
        # ax.set_ylim((self.Y_MIN_NUM, self.Y_MAX_NUM))
        # 重新绘制图形
        ax.figure.canvas.draw()
        fig.canvas.flush_events()
        #plt.draw()


if __name__ == '__main__':
    f = Futures()
    # f.start()
    # # plt.subplots_adjust(left=.09, bottom=.14, right=.94, top=.95, wspace=.20, hspace=0)
    timer = fig.canvas.new_timer(interval=10000)
    timer.add_callback(f.on_timer)
    timer.start()

    cursor = Cursor(ax, useblit=True, color='w',linestyle='--',linewidth=.5)

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