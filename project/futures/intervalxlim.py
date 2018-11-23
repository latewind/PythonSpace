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


fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
x = [1, 2, 3, 4, 5, 51, 52, 53, 54, 55]
y = [4, 3, 4, 5, 4, 3, 4, 5, 6, 4]
ax1.bar(x, y)
ax2.bar(x, y)

# Fix the axis
ax1.spines['right'].set_visible(False)
ax1.yaxis.tick_left()
ax2.spines['left'].set_visible(False)
ax2.yaxis.tick_right()
ax2.tick_params(labelleft='off')
ax1.set_xlim(1, 6)
ax2.set_xlim(51, 56)
plt.show()