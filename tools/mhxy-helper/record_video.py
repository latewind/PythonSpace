import numpy as np
import cv2
import time
import mss

frame_width = 630
frame_height = 420
frame_rate = 20.0
PATH_TO_MIDDLE = "outputpow3.avi"
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(PATH_TO_MIDDLE, fourcc, frame_rate,
                      (frame_width, frame_height))

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 275, "left": 90, "width": 630, "height": 420}

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = np.asarray(sct.grab(monitor))
        img = cv2.resize(img, (630, 420))
        frame = img
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGRA)
        # cv2.putText(frame, "FPS: %f" % (1.0 / (time.time() - last_time)),
        #             (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        out.write(frame)
        cv2.imshow('frame', frame)

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

# Clean up
out.release()
cv2.destroyAllWindows()
