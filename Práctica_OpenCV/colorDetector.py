import cv2
import numpy

h = (100, 125)     # color range to detect.
s = (100, 255)  # saturation range.
v = (20, 255)   # brightness range.

color_low = numpy.array([h[0], s[0], v[0]], numpy.uint8)
color_high = numpy.array([h[1], s[1], v[1]], numpy.uint8)

capture = cv2.VideoCapture('prueba2.mp4')

while True:
    status, frame = capture.read()
    if status:
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color_filter = cv2.inRange(frameHSV, color_low, color_high)  # This is where the color detection is done.
        final_frame = cv2.bitwise_and(frame, frame, mask=color_filter)
        cv2.imshow('SHOW COLOR', final_frame)
        cv2.imshow('FILTER', color_filter)
        cv2.imshow('CAPTURE', frame)
        if cv2.waitKey(1) & 0xFF == ord('e'):  # Press 'e' to exit.
            break
    else:
        break
capture.release()
cv2.destroyAllWindows()
