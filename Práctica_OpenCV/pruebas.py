import cv2
import numpy

h = (100, 125)     # color range
s = (100, 255)  # saturation range.
v = (20, 255)   # brightness range.

color_low = numpy.array([h[0], s[0], v[0]], numpy.uint8)
color_high = numpy.array([h[1], s[1], v[1]], numpy.uint8)

# image = cv2.imread('figure.jpg')
# imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# color_filter = cv2.inRange(imageHSV, color_low, color_high)  # This is where the color detection is done.
# final_image = cv2.bitwise_and(image, image, mask=color_filter)
color_filter = numpy.zeros((400, 600), numpy.uint8)
color_filter[100:300, 200:400] = 255
color_filter[10:30, 20:40] = 255
(outlines, _) = cv2.findContours(color_filter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(color_filter, outlines, -1, (0, 0, 255), 3)

# cv2.imshow('ORIGINAL', image)
cv2.imshow('FILTER', color_filter)
# cv2.imshow('FILTER COLOR', final_image)
print(outlines)

cv2.waitKey(0)
cv2.destroyAllWindows()
