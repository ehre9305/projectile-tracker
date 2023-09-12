#!/usr/bin/env python
import cv2
import math
import time
import camera
import get_coords
import write_data

PRINT_FPS = False

reference_points = []
meters_per_pixel = 0.0036956521739130435  # testing ratio in room, about 2m away
current_meters = 1.715  # kyle's wingspan


def inputNumber(message):
    while True:
        try:
            userInput = float(input(message))
            break
        except ValueError:
            print("Not a valid number. Please try again.")
    return userInput


def get_dist_between_points(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def mouse_callback(event, x, y, flags, param):
    global current_meters, meters_per_pixel
    if event == cv2.EVENT_LBUTTONDOWN:
        reference_points.append((x, y))
        if len(reference_points) == 3:
            reference_points.pop(0)
        if len(reference_points) == 2:
            meters_per_pixel = current_meters / get_dist_between_points(
                reference_points[0], reference_points[1]
            )
            print("meters per pixel: " + str(meters_per_pixel))

    elif event == cv2.EVENT_RBUTTONDOWN:
        current_meters = inputNumber("Enter distance between points in meters: ")


def draw_ruler(frame):
    RULER_COLOR = (255, 255, 0)
    if len(reference_points) != 0:
        for point in reference_points:
            frame = cv2.circle(frame, point, 3, RULER_COLOR)

        if len(reference_points) == 2:
            frame = cv2.line(
                frame, reference_points[0], reference_points[1], RULER_COLOR
            )
            frame = cv2.putText(
                frame,
                str(current_meters) + "m",
                (
                    int((reference_points[0][0] + reference_points[1][0]) / 2),
                    int((reference_points[0][1] + reference_points[1][1]) / 2),
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                RULER_COLOR,
            )

    return frame


last_time = time.time()


def draw_fps(frame, t):
    global last_time
    FPS_COLOR = (0, 255, 0)
    FPS_LOCATION = (0, 40)
    current_time = t

    fps = round(1 / (current_time - last_time), 1)
    if PRINT_FPS and not points_ended:
        print(fps)
    frame = cv2.putText(
        frame,
        str(fps) + "fps",
        FPS_LOCATION,
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        FPS_COLOR,
    )
    last_time = current_time
    return frame


def nothing(x):
    pass


def createWindowAndTrackbars():
    # Create a window
    cv2.namedWindow("image", cv2.WINDOW_GUI_NORMAL)
    cv2.setMouseCallback("image", mouse_callback)
    # create trackbars for color change
    cv2.createTrackbar("HMin", "image", 0, 179, nothing)  # Hue is from 0-179 for Opencv
    cv2.createTrackbar("SMin", "image", 0, 255, nothing)
    cv2.createTrackbar("VMin", "image", 0, 255, nothing)
    cv2.createTrackbar("HMax", "image", 0, 179, nothing)
    cv2.createTrackbar("SMax", "image", 0, 255, nothing)
    cv2.createTrackbar("VMax", "image", 0, 255, nothing)

    cv2.createTrackbar(
        "max y",
        "image",
        0,
        int(camera.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)) - 1,
        nothing,
    )

    # green
    setup = "green"
    if setup == "green":
        cv2.setTrackbarPos("HMin", "image", 13)
        cv2.setTrackbarPos("SMin", "image", 40)
        cv2.setTrackbarPos("VMin", "image", 96)
        cv2.setTrackbarPos("HMax", "image", 42)
        cv2.setTrackbarPos("SMax", "image", 255)
        cv2.setTrackbarPos("VMax", "image", 255)
    elif setup == "red":
        cv2.setTrackbarPos("HMin", "image", 160)
        cv2.setTrackbarPos("SMin", "image", 100)
        cv2.setTrackbarPos("VMin", "image", 140)
        cv2.setTrackbarPos("HMax", "image", 179)
        cv2.setTrackbarPos("SMax", "image", 255)
        cv2.setTrackbarPos("VMax", "image", 255)
    else:
        cv2.setTrackbarPos("HMin", "image", 0)
        cv2.setTrackbarPos("SMin", "image", 0)
        cv2.setTrackbarPos("VMin", "image", 0)
        cv2.setTrackbarPos("HMax", "image", 179)
        cv2.setTrackbarPos("SMax", "image", 255)
        cv2.setTrackbarPos("VMax", "image", 255)


createWindowAndTrackbars()


def filter(frame):
    hMin = cv2.getTrackbarPos("HMin", "image")
    sMin = cv2.getTrackbarPos("SMin", "image")
    vMin = cv2.getTrackbarPos("VMin", "image")

    hMax = cv2.getTrackbarPos("HMax", "image")
    sMax = cv2.getTrackbarPos("SMax", "image")
    vMax = cv2.getTrackbarPos("VMax", "image")

    lower = (hMin, sMin, vMin)
    upper = (hMax, sMax, vMax)

    return cv2.inRange(hsv, lower, upper)


waitTime = 1

# points shape (t, x, y)
initial_time = -1
t_data, y_data, x_data = [], [], []

points_ended = False


def points_started():
    return len(t_data) > 0


def draw_threshold_line(frame):
    return cv2.line(
        img,
        (0, max_y),
        (
            img.shape[1],
            max_y,
        ),
        (255, 0, 255),
    )


def handle_coords(coords, t):
    global initial_time, points_ended
    if not points_ended and coords[1] < max_y:
        if initial_time == -1:
            print("starting")
            initial_time = t
            t_data.append(0)
        else:
            t_data.append(t - initial_time)
        x_data.append(coords[0] * meters_per_pixel)
        y_data.append((max_y - coords[1]) * meters_per_pixel)
        write_data.write_points(t_data, x_data, y_data)
        if len(t_data) > 1:
            write_data.create_lines(t_data, x_data, y_data)
    elif points_started():
        points_ended = True


while 1:
    before_frame_time = time.time()
    img, t = camera.get_frame_and_fps()

    # Create HSV Image and threshold into a range.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    filt_img = filter(img)

    max_y = cv2.getTrackbarPos("max y", "image")

    contours = get_coords.get_contours(filt_img)
    biggest_contour = get_coords.get_biggest_contour(contours)
    coords = get_coords.get_contour_coords(biggest_contour)

    TARGET_COLOR = (0, 255, 255)
    img = cv2.drawContours(img, contours, -1, tuple(n * 0.8 for n in TARGET_COLOR))

    if coords != None:
        handle_coords(coords, t)
        img = cv2.circle(img, coords, 5, TARGET_COLOR, 3)
        img = cv2.drawContours(img, [biggest_contour], 0, TARGET_COLOR)

    img = draw_ruler(img)
    img = draw_fps(img, t)
    img = draw_threshold_line(img)

    cv2.imshow("image", img)

    if PRINT_FPS and not points_ended:
        print("total work time" + str(time.time() - before_frame_time))
    # Wait longer to prevent freeze for videos.
    if cv2.waitKey(waitTime) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()

# print(*zip(t_data, x_data, y_data), sep=",\n")

camera.camera.release()
