#!/usr/bin/env python
import cv2 as cv
import numpy as np


class ranges:
    hue = (170, 180)
    sat = (75, 255)
    val = (75, 255)

    def get_limit(n: int):
        return (ranges.hue[n], ranges.sat[n], ranges.val[n])


EROSION_AMOUNT = 16
EROSION_KERNEL = np.ones((EROSION_AMOUNT, EROSION_AMOUNT), np.uint8)


def filter_frame(frame):
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frame = cv.inRange(frame, ranges.get_limit(0), ranges.get_limit(1))
    frame = cv.erode(frame, EROSION_KERNEL, iterations=1)

    return frame


def get_contours(frame):
    contours, _ = cv.findContours(frame, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    return contours


def get_biggest_contour(contours):
    if len(contours) == 0:
        return None
    return max(contours, key=cv.contourArea)


def get_contour_coords(contour):
    if contour is None:
        return None
    moments = cv.moments(contour)
    if moments["m00"] == 0:
        return None
    cx = int(moments["m10"] / moments["m00"])
    cy = int(moments["m01"] / moments["m00"])
    return (cx, cy)
