import cv2 as cv
import time

camera = cv.VideoCapture(0)

last_frame = None


def get_frame():
    global last_frame
    if last_frame == None:
        last_frame = camera.read()[1], time.time()
        return last_frame
    else:
        print("double")
        out = last_frame
        time.sleep(max(0.016 - time.time() + last_frame[1], 0))
        last_frame = None
        return out[0], time.time()
