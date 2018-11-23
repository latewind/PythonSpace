import pyautogui as pag
screenWidth, screenHeight = pag.size()

import random
import time

while True:
    x = random.randint(0, screenWidth)
    y = random.randint(0, screenHeight)
    pag.moveTo(x, y)
    time.sleep(random.randint(1, 300))