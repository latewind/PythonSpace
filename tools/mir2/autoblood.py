# -*- coding: utf-8 -*-
import win32process  # 进程模块
from win32con import PROCESS_ALL_ACCESS  # Opencress 权限
import win32con
import win32api  # 调用系统模块
import ctypes  # C语言类型
from win32gui import FindWindow  # 界面
from threading import Thread

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


class Mir2GameHelper:
    def __init__(self, win_class, win_title):
        self.base_address = 0x00A10000
        self.offset_1 = 0x00510548
        self.offset_2 = 0x218

        self.win_class = win_class
        self.win_title = win_title

        self.kernel32 = ctypes.windll.LoadLibrary("kernel32.dll")  # 加载动态链接库
        self.hwnd = FindWindow(self.win_class, self.win_title)  # 获取窗口句柄
        h_pid, pid = win32process.GetWindowThreadProcessId(self.hwnd)  # 获取窗口ID
        self.h_process = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, pid)  # 获取进程句柄

        self.blood_address = 0

        self.LOOP = True

        self.thread = Thread(target=self.add_blood)

    def attach_win(self):
        pass

    def read_memory(self, address, buff_len):
        mem_value = ctypes.c_ulong()
        self.kernel32.ReadProcessMemory(int(self.h_process), address, ctypes.byref(mem_value), buff_len, None)  # 读内存

        return mem_value.value

    def close_helper(self):
        self.LOOP = False
        print("is stopping")
        time.sleep(2)
        self.thread.join()
        win32api.CloseHandle(self.h_process)  # 关闭句柄
        print("close ")

    def auto_add_blood(self):
        print("start thread")
        self.thread.start()

    def add_blood(self):
        while self.LOOP:
            blood = self.read_memory(self.get_blood_address() + self.offset_2, 4)
            if blood < 2000:
                print("add blood")
                win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, 49, 0)  # 发送1键
                win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, 49, 0)
            time.sleep(0.6)

    def get_blood_address(self):
        if self.blood_address == 0:
            self.blood_address = self.read_memory(self.base_address + self.offset_1, 4)
        return self.blood_address


if __name__ == '__main__':
    # main()
    helper = Mir2GameHelper("TFrmMain", "昆仑长留战区 - 一刀九九九")
    helper.auto_add_blood()
    a = input("end:")
    print(a)
    if a == "end":
        helper.close_helper()
