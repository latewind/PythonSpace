import datetime
import imutils
import time
import cv2

deff_point = 3
base_point = [
    (298.0, 161.0),  # A
    (403.0, 302.5),  # C
    (200.0, 363.5),  # D
    (498.5, 221.5),  # B
    (97.5, 263.0),  # E
]


def ignore_base_point(p):
    x = float(p[0])
    y = float(p[1])
    for _ in base_point:
        if (_[0] - deff_point <= x <= _[0] + deff_point) and (_[1] - deff_point <= y <= _[1] + deff_point):
            return True
    return False


camera = cv2.VideoCapture('outputpig3.avi')
# camera = cv2.VideoCapture('outputpig3.avi')
# camera = cv2.VideoCapture('outputroworg.avi')
# camera = cv2.VideoCapture('pig.mp4')
# camera = cv2.VideoCapture('output.avi')
frame_count = 0
moving_line = []
# 初始化视频流的第一帧
firstFrame = None

firstFrame = cv2.imread("res/bgnormal.jpg", cv2.IMREAD_COLOR)
# firstFrame = cv2.imread("res/bgnormal.jpg", cv2.IMREAD_GRAYSCALE)
# firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)
inc = 1
# 遍历视频的每一帧
while True:
    frame_count = frame_count + 1
    # 获取当前帧并初始化occupied/unoccupied文本
    (grabbed, frame) = camera.read()
    text = "Unoccupied"

    # 如果不能抓取到一帧，说明我们到了视频的结尾
    if not grabbed:
        break

    # 调整该帧的大小，转换为灰阶图像并且对其进行高斯模糊
    # frame = imutils.resize(frame, width=500)
    cv2.imshow('frame', cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA))

    gray = frame
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    # gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # 如果第一帧是None，对其进行初始化
    if firstFrame is None:
        firstFrame = gray
        continue
    # 计算当前帧和第一帧的不同
    frameDelta = cv2.absdiff(firstFrame, gray)

    thresh = cv2.threshold(cv2.cvtColor(frameDelta, cv2.COLOR_BGR2GRAY), 25, 255, cv2.THRESH_BINARY)[1]
    #
    # # 扩展阀值图像填充孔洞，然后找到阀值图像上的轮廓
    # thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)
    moving_point_list = []
    # 遍历轮廓
    moving_point = 0
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 200 or cv2.contourArea(c) > 10000:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        # 计算轮廓的边界框，在当前帧中画出该框
        (x, y, w, h) = cv2.boundingRect(c)
        moving_point_list.append((x + w / 2, y + h / 2))
        # print(x + w / 2, ',', y + h / 2)
        if ignore_base_point((x + w / 2, y + h / 2)):
            continue
        else:
            moving_point = moving_point + 1

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    if moving_point >= 3:
        print(frame_count)
        print(moving_point_list)
        moving_line.append(moving_point)
    moving_point_list = []
    moving_point = 0

    # draw the text and timestamp on the frame
    # 在当前帧上写文字以及时间戳
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # 显示当前帧并记录用户是否按下按键
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    cv2.imshow("gray", gray)
    key = cv2.waitKey(1)
    inc = inc + 1
    # 如果q键被按下，跳出循环
    if key == ord("q"):
        break
    if frame_count > 50:
        time.sleep(0.2)
    time.sleep(0.2)

print(frame_count)
print(moving_line)
# 清理摄像机资源并关闭打开的窗口
camera.release()
cv2.destroyAllWindows()


def get_close_in_point(point, points):
    diff = 10000
    close_point = point
    x1 = point[0]
    y1 = point[1]
    for p in points:
        x2 = p[0]
        y2 = p[1]
        d = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        if d < diff:
            diff = d
            close_point = p
    return close_point
