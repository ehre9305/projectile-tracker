import cv2 as cv

camera = cv.VideoCapture(0)


def get_frame():
    return camera.read()[1], camera.get(cv.CAP_PROP_POS_MSEC) / 1000
