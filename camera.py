import cv2 as cv
import time

camera = cv.VideoCapture(0)


def get_frame_and_fps():
    return camera.read()[1], time.time()
