import cv2
import imutils as imutils
import numpy as np

from Constants import Constants


def getSlope(point):
    try:
        return float(point[1]) / float(point[0])
    except:
        return 1000


def getSlopeDuo(first, second):
    try:
        return float(first[1] - second[1]) / float(first[0] - second[0])
    except:
        return 1000


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

if __name__ == '__main__':
    c = Constants()
    c.readValues()
    cap = cv2.VideoCapture(0)


    # mouse callback function
    def draw_circle(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            print(x,y)


    # Create a black image, a window and bind the function to window
    img = np.zeros((512, 512, 3), np.uint8)
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", draw_circle)

    while True:
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, c.lowArray, c.highArray)
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        largerThan500 = []
        for cnt in contours:
            if (cv2.contourArea(cnt) > 1000):
                largerThan500.append(cnt)
        contours = largerThan500

        try:

            cntsSorted = sorted(contours, key=lambda x: cv2.contourArea(x))
            cntsSorted.reverse()
            cnt = cntsSorted[0]

            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            points = []
            for point in box:
                points.append(point)

            points.sort(key=getSlope, reverse=True)

            cv2.line(frame, (points[0][0], points[0][1]), (points[3][0], points[3][1]), (0, 255, 0), 2)  # Green
            cv2.line(frame, (points[1][0], points[1][1]), (points[2][0], points[2][1]), (255, 255, 0), 2)  # Blue

            line1 = []
            line1.append(points[0])
            line1.append(points[3])

            line2 = []
            line2.append(points[1])
            line2.append(points[2])

            x,y = line_intersection(line1, line2)

            print("Points: ", points[0],points[1],points[2],points[3])
            print("Point 1 Slope: ", getSlope(points[0]))
            print("Point 2 Slope: ", getSlope(points[1]))
            print("Point 3 Slope: ", getSlope(points[2]))
            print("Point 4 Slope: ", getSlope(points[3]))
            print("Center Point: (",x,",",y,")")

            cv2.circle(frame, (int(x), int(y)), 10, (0, 0, 255), -1)
            cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

        except Exception as err:
            print(err)

        # cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
        cv2.imshow("frame", frame)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
