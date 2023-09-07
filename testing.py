import cv2 as cv

camera = cv.VideoCapture("/home/kyle/Documents/apphys/IMG_0066.mov")



# Create a window
cv2.namedWindow("image", cv2.WINDOW_NORMAL)


def createWindowAndTrackbars():
    # Create a window
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    # create trackbars for color change
    cv2.createTrackbar("HMin", "image", 0, 179, nothing)  # Hue is from 0-179 for Opencv
    cv2.createTrackbar("SMin", "image", 0, 255, nothing)
    cv2.createTrackbar("VMin", "image", 0, 255, nothing)
    cv2.createTrackbar("HMax", "image", 0, 179, nothing)
    cv2.createTrackbar("SMax", "image", 0, 255, nothing)
    cv2.createTrackbar("VMax", "image", 0, 255, nothing)

    # Set default value for MAX HSV trackbars.
    cv2.setTrackbarPos("HMax", "image", 179)
    cv2.setTrackbarPos("SMax", "image", 255)
    cv2.setTrackbarPos("VMax", "image", 255)


createWindowAndTrackbars()

# Initialize to check if HSV min/max value changes
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0


# create trackbars for color change
waitTime = 1

while 1:
    img = testing.get_frame()

    hMin = cv2.getTrackbarPos("HMin", "image")
    sMin = cv2.getTrackbarPos("SMin", "image")
    vMin = cv2.getTrackbarPos("VMin", "image")

    hMax = cv2.getTrackbarPos("HMax", "image")
    sMax = cv2.getTrackbarPos("SMax", "image")
    vMax = cv2.getTrackbarPos("VMax", "image")

    # Set minimum and max HSV values to display
    lower = (hMin, sMin, vMin)
    upper = (hMax, sMax, vMax)

    # Create HSV Image and threshold into a range.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    filt_img = cv2.inRange(hsv, lower, upper)
    img = cv2.bitwise_and(img, img, mask=filt_img)

    cv2.imshow(
        "image",
        cv2.circle(
            img, get_coords.get_coords_from_frame(filt_img), 20, (0, 255, 255), 3
        ),
    )

    # Wait longer to prevent freeze for videos.
    if cv2.waitKey(waitTime) & 0xFF == ord("q"):
        break


cv2.destroyAllWindows()
