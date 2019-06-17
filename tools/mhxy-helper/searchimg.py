import time

import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageGrab


def sleep(second):
    def _sleep(func):
        def wrapper(*args):
            time.sleep(second)
            return func(*args)

        return wrapper

    return _sleep


def search_img(img_path, area=(0, 0, 1270, 800)):
    time.sleep(2)
    img_screen = ImageGrab.grab(area)
    img_np = np.array(img_screen)

    template = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    img = img_np.copy()

    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val > 0.65:
        print(max_loc)
        return max_loc
    return None
