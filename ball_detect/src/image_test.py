import cv2

capture = cv2.VideoCapture(1)
while True:
    ret, frame = capture.read()
    if ret:
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
    else:
        break
