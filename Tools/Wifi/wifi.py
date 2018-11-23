from pywifi import *
import time

wifi = PyWiFi()
iface = wifi.interfaces()[0]
iface.scan()

#time.sleep(200)
print(iface.scan_results())