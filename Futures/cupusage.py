'''
来自zhihu
'''
import psutil as p
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib.ticker import Formatter, FixedLocator


POINTS = 300

fig,ax = plt.subplots()

ax.set_ylim([0, 100])
ax.set_xlim([0, POINTS])
ax.set_autoscale_on(False)

# 坐标轴刻度
ax.set_xticks([])
ax.set_yticks(range(0, 101, 10))
ax.grid(True)

user = [None] * POINTS
nice = [None] * POINTS
sys = [None] * POINTS
idle = [None] * POINTS

l_user, = ax.plot(range(POINTS), user, label = 'User %')
l_nice, = ax.plot(range(POINTS), nice, label = 'Nice %')
l_sys, = ax.plot(range(POINTS), sys, label = 'Sys %')
l_idle, = ax.plot(range(POINTS), idle, label = 'Idle %')


ax.legend(loc = 'upper center',
           ncol = 4, prop = font_manager.FontProperties(size = 10))

bg = fig.canvas.copy_from_bbox(ax.bbox)

def prepare_cpu_usage():
    """
    获取 cpu已经运行的时间
    :return:
    """
    t = p.cpu_times()
    if hasattr(t, 'nice'):
        return [t.user, t.nice, t.system, t.idle]
    else:
        return [t.user, 0, t.system, t.idle]

before = prepare_cpu_usage()

def get_cpu_usage():
    global before

    now = prepare_cpu_usage()
    # 现在运行的时候和上次获取的运行时间相减，获取时间差
    delta = [now[i] - before[i] for i in range(len(now))]
    total = sum(delta)
    print(total)
    before = now
    # 各个时间除以总时间差，就是所占比例，+0.1是因为每隔0.1统计一次时间，总时间上
    return [(100.0*dt)/(total+0.1) for dt in delta]

def OnTimer(ax):
    global user,nice,sys,idle,bg

    tmp = get_cpu_usage()

    user = user[1:] + [tmp[0]]
    nice = nice[1:] + [tmp[1]]
    sys = sys[1:] + [tmp[2]]
    idle = idle[1:] + [tmp[3]]

    l_user.set_ydata(user)
    l_nice.set_ydata(nice)
    l_sys.set_ydata(sys)
    l_idle.set_ydata(idle)

    ax.draw_artist(l_user)
    ax.draw_artist(l_nice)
    ax.draw_artist(l_sys)
    ax.draw_artist(l_idle)

    ax.figure.canvas.draw()

timer = fig.canvas.new_timer(interval=100)
timer.add_callback(OnTimer,ax)
timer.start()
plt.show()