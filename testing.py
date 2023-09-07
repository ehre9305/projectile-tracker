import cv2 as cv

camera = cv.VideoCapture("/home/kyle/Documents/apphys/IMG_0066.mov")


def get_frame():
    ret, frame = camera.read()
    if ret:
        return frame
    else:
        camera.set(cv.CAP_PROP_POS_FRAMES, 0)
        return get_frame()
