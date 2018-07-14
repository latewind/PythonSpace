import time
import requests
import matplotlib.pyplot as plt
from threading import Thread
import datetime
import random
import numpy as np
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from mpl_toolkits.axes_grid1 import host_subplot


column_index = ['名称', '位置', '开盘价', '最高价', '最低价', '昨日收盘价', '买价', '卖价', '最新价', '结算价', '昨结算', '买量', '卖量', '持仓量', '成交量']
URL = "http://hq.sinajs.cn/?_=0/&list=CU1809"

fig = plt.figure()
# ax = host_subplot(111)

ax = fig.add_subplot(1, 1, 1)


# plt.axis([0, 1, 86400, 1.0 *50000])



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
        self.Y_MAX_NUM = 48999
        self.Y_MIN_NUM = 48999

        self.random = random.Random()

        ax.plot(self.times, self.prices, '-', [self.start_date, self.end_date], [48700, 50000], '-')
        ax.set_xlim(self.start_date, self.end_date)
        ax.xaxis.set_minor_locator(HourLocator(range(0, 25, 6)))
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
        # ax.set_ylim((self.Y_MIN_NUM, self.Y_MAX_NUM))
        ax.grid()
        fig.autofmt_xdate()
        pass

    def _fetch_data(self):
        cur_time = time.time()
        time_dlt = int(cur_time - self.today_start_time)

        t = int(round(cur_time * 1000))

        ctx = requests.get(URL)
        data = ctx.text.strip('varhq_str_CU1809=" ;\n').split(",")
        price = float(data[8])
        #
        price = self._gen_C1809_price()
        self.prices.append(price)
        self.times.append(datetime.datetime.now())
        print(float(price))

        if price > self.Y_MAX_NUM:
            self.Y_MAX_NUM = price * 1.001
        if price < self.Y_MIN_NUM:
            self.Y_MIN_NUM = price * 0.999

    def _gen_C1809_price(self):

        return float(self.random.randint(48000, 50000))

    def thread_start(self):
        while self.flag:
            time.sleep(3)
            self._fetch_data()
            # self.range_s += self.range_step
            # self.range_e += self.range_step
            # t = np.arange(self.range_s, self.range_e, self.range_step)
            # ydata = np.sin(4 * np.pi * t)
            # 更新数据
            ax.plot(self.times, self.prices)

            # 更新坐标
            # ax.set_ylim((self.Y_MIN_NUM, self.Y_MAX_NUM))
            # 重新绘制图形
            plt.draw()

    def start(self):
        self.flag = True
        # 创建并启动新线程
        t = Thread(target=self.thread_start)
        t.start()


if __name__ == '__main__':
    f = Futures()
    f.start()
    plt.show()
