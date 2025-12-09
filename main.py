import cv2 as cv
import numpy as np
import time

capture_video = cv.VideoCapture(0)

time.sleep(1)

count = 0
background = 0

for i in range(60):
    return_val, background = capture_video.read()
    if return_val == False:
        continue

background = np.flip(background,1)

while capture_video.isOpened():
    return_val, img = capture_video.read()
    if not return_val:
        break
    count+=1
    img = np.flip(img, 1)

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # setting the lower and upper range for blue color
    lower_blue = np.array([90, 40, 40])
    upper_blue = np.array([130, 255, 255])
    mask1 = cv.inRange(hsv, lower_blue, upper_blue)

    # Note: Blue doesn't typically wrap around HSV like red does, 
    # so we don't need a second mask range for blue

    mask1 = cv.morphologyEx(mask1, cv.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask1 = cv.dilate(mask1, np.ones((3, 3), np.uint8), iterations=2)

    mask2 = cv.bitwise_not(mask1)

    res1 = cv.bitwise_and(background, background, mask = mask1)
    res2 = cv.bitwise_and(img, img, mask = mask2)

    final_output = cv.addWeighted(res1, 1, res2, 1, 0)

    cv.imshow('Invisible T-shirt', final_output)

    if cv.waitKey(1) & 0xFF == ord('b'):
        break