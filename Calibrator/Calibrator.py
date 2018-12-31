import cv2
import numpy as np

from Constants import Constants

c = Constants()

cap = cv2.VideoCapture(0)

def nothing(x):
    pass

# Creating a window for later use
cv2.namedWindow('result')

# Starting with 100's to prevent error while masking
lH, lS, lV, hH, hS, hV = c.readIndividualValues()

# Creating track bar
cv2.createTrackbar('Low H', 'result',0,179,nothing)
cv2.createTrackbar('Low S', 'result',0,255,nothing)
cv2.createTrackbar('Low V', 'result',0,255,nothing)

cv2.createTrackbar('High H', 'result',0,179,nothing)
cv2.createTrackbar('High S', 'result',0,255,nothing)
cv2.createTrackbar('High V', 'result',0,255,nothing)

while True:

    _, frame = cap.read()

    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    lH = cv2.getTrackbarPos('Low H', 'result')
    lS = cv2.getTrackbarPos('Low S', 'result')
    lV = cv2.getTrackbarPos('Low V', 'result')
    hH = cv2.getTrackbarPos('High H', 'result')
    hS = cv2.getTrackbarPos('High S', 'result')
    hV = cv2.getTrackbarPos('High V', 'result')

    c.writeValues(lH, lS, lV, hH, hS, hV)

    # Normal masking algorithm
    lower = np.array([lH, lS, lV])
    upper = np.array([hH, hS, hV])

    mask = cv2.inRange(hsv, lower, upper)

    result = cv2.bitwise_and(frame,frame,mask = mask)

    cv2.imshow('result',result)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()