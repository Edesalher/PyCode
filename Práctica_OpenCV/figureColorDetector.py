import cv2
import numpy
import imutils

h = (                   # Colors range
    ('Red1', 0, 10),
    ('Red2', 175, 180),
    ('Yellow', 10, 32),
    ('Blue', 100, 125),
    ('Orange', 11, 19),
    ('Green', 36, 70),
    ('Violet', 130, 145)
)
s = (100, 125)          # saturation range.
v = (20, 255)           # brightness range


# This function only finds the following figures: square, rectangle, triangle, pentagon and circle.
def find_figures(picture):
    # Finding all the edges of the figures in the image with the canny algorithm.
    canny_outlines = cv2.Canny(picture, 10, 150)
    # canny_outlines = cv2.dilate(canny_outlines, None, iterations=1)
    # outlines_canny = cv2.erode(outlines_canny, None, iterations=1)
    (contours, _) = cv2.findContours(canny_outlines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    figure_list = []
    for contour in contours:
        precision = 0.01 * cv2.arcLength(contour, True)
        # Improving the contour of the found image.
        approx_contour = cv2.approxPolyDP(contour, precision, True)
        # Closing the figure of interest.
        x, y, width, high = cv2.boundingRect(approx_contour)

        if len(approx_contour) == 4:
            aspect_ratio = float(width / high)
            if aspect_ratio == 1:
                figure_list += [x, y, 'Square', approx_contour],
            else:
                figure_list += [x, y, 'Rectangle', approx_contour],
        elif len(approx_contour) == 3:
            figure_list += [x, y, 'Triangle', approx_contour],
        elif len(approx_contour) == 5:
            figure_list += [x, y, 'Pentagon', approx_contour],
        elif len(approx_contour) > 10:
            figure_list += [x, y, 'Circle', approx_contour],
    # cv2.drawContours(image, contours, -1, (0, 0, 255), 2)
    return figure_list


# This function only detect the following colors: red, yellow, blue, orange, green and violet.
def find_colors(picture_hsv):
    color_list = []
    for hue in h:
        color, low_hue, high_hue = hue
        low_color = numpy.array([low_hue, s[0], v[0]], numpy.uint8)
        high_color = numpy.array([high_hue, s[1], v[1]], numpy.uint8)
        filtered_image = cv2.inRange(picture_hsv, low_color, high_color)  # This is where the color detection is done.
        # If no color was detected, the list of contours will be empty because there is no figure matching that color.
        (contours, _) = cv2.findContours(filtered_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            color_list += color,
    return color_list


image = cv2.imread('figure640x480color.jpeg')
# image = imutils.resize(image, 640, 480)

# Color conversion
imageGRAY = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Figure finder
figures = find_figures(imageGRAY)

for figure_detected in figures:
    positionX, positionY, figure, contour_found = figure_detected
    # A black background is created as the image base.
    background = numpy.zeros((480, 640), dtype=numpy.uint8)
    figure_of_interest = cv2.drawContours(background, [contour_found], -1, 255, -1)
    # Creating a new image that only contains the figure to which the color will be detected.
    new_image = cv2.bitwise_and(imageHSV, imageHSV, mask=figure_of_interest)
    color_detected = find_colors(new_image)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, f'{figure} {color_detected[0]}', (positionX + 3, positionY - 12), font, 0.6, (0, 0, 0), 2)
    cv2.waitKey(0)
    cv2.imshow('IMAGE', image)

# cv2.imshow('IMAGE', image)

cv2.waitKey(0)
cv2.destroyAllWindows()
