import cv2
import numpy

h = (100, 125)     # color range
s = (100, 255)  # saturation range.
v = (20, 255)   # brightness range.

color_low = numpy.array([h[0], s[0], v[0]], numpy.uint8)
color_high = numpy.array([h[1], s[1], v[1]], numpy.uint8)

capture = cv2.VideoCapture('prueba2.mp4')

while True:
    status, frame = capture.read()
    if status:
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color_filter = cv2.inRange(frameHSV, color_low, color_high)
        (contours, _) = cv2.findContours(color_filter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for outline in contours:
            area = cv2.contourArea(outline)
            if area > 3000:
                M = cv2.moments(outline)
                if M['m00'] == 0:
                    M['m00'] = 1
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])
                cv2.circle(frame, (x, y), 7, (0, 0, 255), -1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, f'{x},{y}', (x+10, y), font, 0.75, (0, 0, 255), 1, cv2.LINE_AA)
                new_outline = cv2.convexHull(outline)
                cv2.drawContours(frame, [new_outline], 0, (0, 0, 255), 3)
        cv2.imshow('CAPTURE', frame)
        if cv2.waitKey(1) & 0xFF == ord('e'):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()
