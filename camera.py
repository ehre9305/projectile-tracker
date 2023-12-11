import cv2 as cv
import time

camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_EXPOSURE, 10);


def get_frame_and_fps():
    return camera.read()[1], time.time()
