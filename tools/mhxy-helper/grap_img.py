import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageGrab


img_screen = ImageGrab.grab((1200, 55, 1265, 100))
img_screen.save("h.bmp")