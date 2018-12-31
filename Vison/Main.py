import cv2

from Constants import Constants

if __name__ == '__main__':
    Constants.readValues()
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, Constants.lowArray, Constants.highArray)
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
        cv2.imshow("frame",frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
