import datetime
import imutils
import time
import cv2


camera = cv2.VideoCapture('outputpig12')
# camera = cv2.VideoCapture('pig.mp4')
# camera = cv2.VideoCapture('output.avi')


# 初始化视频流的第一帧
firstFrame = None

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
fgbg = cv2.bgsegm.createBackgroundSubtractorGMG(initializationFrames=5)

# 遍历视频的每一帧
while True:
    # 获取当前帧并初始化occupied/unoccupied文本
    (grabbed, frame) = camera.read()
    text = "Unoccupied"

    # 如果不能抓取到一帧，说明我们到了视频的结尾
    if not grabbed:
        break
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)  # 过滤噪声

    erode = cv2.erode(fgmask, (21, 21), iterations=1)
    dilate = cv2.dilate(fgmask, (21, 21), iterations=1)

    (cnts, _) = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)

    # 遍历轮廓
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 800:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        # 计算轮廓的边界框，在当前帧中画出该框
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

# draw the text and timestamp on the frame
    # 在当前帧上写文字以及时间戳
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    #显示当前帧并记录用户是否按下按键
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", erode)
    cv2.imshow("Frame Delta", dilate)
    key = cv2.waitKey(1)

    # 如果q键被按下，跳出循环
    if key == ord("q"):
        break
    time.sleep(0.5)

# 清理摄像机资源并关闭打开的窗口
camera.release()
cv2.destroyAllWindows()