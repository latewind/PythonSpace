from ctypes import *

dll = CDLL("hello.dll")
dll = cdll.LoadLibrary('hello.dll')

print(dll.add(1, 2))
