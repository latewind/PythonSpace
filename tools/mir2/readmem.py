# -*- coding: utf-8 -*-
import win32process  # 进程模块
from win32con import PROCESS_ALL_ACCESS  # Opencress 权限
import win32con
import win32api  # 调用系统模块
import ctypes  # C语言类型
from win32gui import FindWindow  # 界面

import time


# 对游戏的一个读操作，读取血量。

def get_process_id(address, bufflength):
    pid = ctypes.c_ulong()  # 设置

    kernel32 = ctypes.windll.LoadLibrary("kernel32.dll")  # 加载动态链接库
    hwnd = FindWindow("TFrmMain", "昆仑长留战区 - 一刀九九九")  # 获取窗口句柄
    h_pid, pid = win32process.GetWindowThreadProcessId(hwnd)  # 获取窗口ID
    h_process = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, pid)  # 获取进程句柄

    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 49, 0)  # 发送1键
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, 49, 0)

    time.sleep(1)
    addr = ctypes.c_ulong()
    kernel32.ReadProcessMemory(int(h_process), address, ctypes.byref(addr), bufflength, None)  # 读内存
    win32api.CloseHandle(h_process)  # 关闭句柄
    return addr.value


def main():
    base_address = 0x00A10000
    offset_1 = 0x00510548
    offset_2 = 0x218

    addr = get_process_id(base_address + offset_1, 4)
    print(hex(addr))
    blood = get_process_id(addr + offset_2, 4)
    print(blood)
    # ret = addr + 0x1C
    # ret2 = GetProcssID(ret, 4)
    # ret3 = ret2 + 0x28
    # ret4 = GetProcssID(ret3, 4)


if __name__ == '__main__':
    main()
