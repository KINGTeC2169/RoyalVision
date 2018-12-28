from threading import Thread
import cv2
from src.Constants import Constants


class ImageThread(Thread):
    def __init__(self, mat):
        Thread.__init__(self)
        self.mat = mat
        pass

    def __run__(self):

        hsv = cv2.cvtColor(self.mat, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, Constants.lower_red, Constants.upper_red)
        res = cv2.bitwise_and(self.mat, self.mat, mask=mask)
