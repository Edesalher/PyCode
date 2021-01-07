import cv2
import numpy

h = (100, 125)  # color range to detect.
s = (100, 255)  # saturation range.
v = (20, 255)   # brightness range.

# Setting the arrays for the color to detect.
lower_color = numpy.array([h[0], s[0], v[0]], numpy.uint8)
upper_color = numpy.array([h[1], s[1], v[1]], numpy.uint8)

# To read a video file.
capture = cv2.VideoCapture('Files/test.mp4')

while capture.isOpened():
    # Capture frame-by-frame.
    ret, frame = capture.read()
    if ret:
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        filtered_frame = cv2.inRange(frameHSV, lower_color, upper_color)  # This is where the color detection is done.
        final_frame = cv2.bitwise_and(frame, frame, mask=filtered_frame)
        # Displaying the corresponding frames.
        cv2.imshow('SHOW COLOR DETECTED', final_frame)
        cv2.imshow('COLOR DETECTED', filtered_frame)
        cv2.imshow('CAPTURE', frame)
        if cv2.waitKey(1) & 0xFF == ord('e'):  # Press 'e' to exit.
            break
    else:
        break

# When everything done, release the capture an so on.
capture.release()
cv2.destroyAllWindows()
