import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageGrab


img_screen = ImageGrab.grab((0, 0, 1200, 800))
img_np = np.array(img_screen)
# img = cv2.imread("lena.jpg", cv2.IMREAD_COLOR)
img2 = img_np.copy()
template = cv2.imread("screen/world_story_act_icon.bmp", cv2.IMREAD_UNCHANGED)
# template = cv2.imread("screen/normal_task_active_collapsed.bmp", cv2.IMREAD_UNCHANGED)
w, h,l = template.shape

# 6 中匹配效果对比算法
# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
methods = ['cv2.TM_CCOEFF_NORMED']
for meth in methods:
    img = img2.copy()

    method = eval(meth)

    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(cv2.minMaxLoc(res),meth)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + h, top_left[1] + w)

    cv2.rectangle(img, top_left, bottom_right, 255, 2)

    plt.subplot(221), plt.imshow(img2, cmap="gray")
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(222), plt.imshow(template, cmap="gray")
    plt.title('template Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(223), plt.imshow(res, cmap="gray")
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(224), plt.imshow(img, cmap="gray")
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.show()