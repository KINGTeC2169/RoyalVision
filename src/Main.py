import cv2

if __name__ == '__main__':
    input = cv2.VideoCapture(0)
    mat = input.read()