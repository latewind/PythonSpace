import re
import time
import win32gui

import ntsecuritycon
import win32con
from win32gui import *

import win32security
import win32api
import sys
import time
from ntsecuritycon import *

titles = set()
simulator_name = '《梦幻西游》手游'


# simulator_name = '按键精灵'

def AdjustPrivilege(priv, enable=1):
    # Get the process token.
    flags = TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY
    htoken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
    # Get the ID for the system shutdown privilege.
    id = win32security.LookupPrivilegeValue(None, priv)
    # Now obtain the privilege for this process.
    # Create a list of the privileges to be added.
    if enable:
        newPrivileges = [(id, SE_PRIVILEGE_ENABLED)]
    else:
        newPrivileges = [(id, 0)]
    # and make the adjustment.
    win32security.AdjustTokenPrivileges(htoken, 0, newPrivileges)


def get_win_handler(hwnd, mouse):
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        titles.add(GetWindowText(hwnd))


EnumWindows(get_win_handler, 0)
win_names = []
for title in titles:
    if title:
        win_names.append(title)
for title in win_names:
    if title.find(simulator_name) != -1:

        hwnd = win32gui.FindWindow(0, title)
        # win32gui.Set
        hwnd = win32gui.FindWindow(0, title)
        size = win32gui.GetWindowRect(hwnd)
        win32gui.MoveWindow(hwnd, -10, 0, size[2] - size[0], size[3] - size[1], 1)
        # win32gui.MoveWindow(hwnd, 0, 0, 1024, 1024, 1)
        # win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0,
        #                       size[2] - size[0],
        #                       size[3] - size[1], win32con.SWP_SHOWWINDOW)
