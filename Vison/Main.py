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


if __name__ == '__main__':
    c = Constants()
    c.readValues()
    cap = cv2.VideoCapture(0)
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

            x1 = points[0][0]
            y1 = points[0][1]
            x0 = points[1][0]
            y0 = points[1][1]
            m0 = getSlopeDuo(points[3], points[0])
            m1 = getSlopeDuo(points[2], points[1])

            print("Point 1 Slope: ", getSlope(points[0]))
            print("Point 2 Slope: ", getSlope(points[1]))
            print("Point 3 Slope: ", getSlope(points[2]))
            print("Point 4 Slope: ", getSlope(points[3]))
            print("Line 1 Slope: ", m0)
            print("Line 2 Slope: ", m1)

            y = (x0 - x1 + y1 * m1 - y0 * m0) / (m1 - m0)
            x = x0 + m0 * (y - y0)

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
