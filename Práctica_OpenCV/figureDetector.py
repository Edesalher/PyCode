import cv2
import numpy
import imutils


# This function just find the next figures: square, rectangle, triangle, pentagon and circle.
def find_figures(picture):
    canny_outlines = cv2.Canny(picture, 10, 150)
    (contours, _) = cv2.findContours(canny_outlines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    figure = []
    for contour in contours:
        precision = 0.01 * cv2.arcLength(contour, True)
        approx_contour = cv2.approxPolyDP(contour, precision, True)
        # Closing the figure of interest
        x, y, width, high = cv2.boundingRect(approx_contour)

        if len(approx_contour) == 4:
            aspect_ratio = float(width / high)
            if aspect_ratio == 1:
                figure += [x, y, 'Square'],
            else:
                figure += [x, y, 'Rectangle'],
        elif len(approx_contour) == 3:
            figure += [x, y, 'Triangle'],
        elif len(approx_contour) == 5:
            figure += [x, y, 'Pentagon'],
        elif len(approx_contour) > 10:
            figure += [x, y, 'Circle'],
    cv2.drawContours(image, contours, -1, (0, 0, 255), 2)
    return figure


image = cv2.imread('figure640x480.jpeg')
# image = imutils.resize(image, 640, 480)

# Color conversion
imageGRAY = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Figure finder
figures = find_figures(imageGRAY)

for figure_detected in figures:
    positionX, positionY, text = figure_detected
    cv2.putText(image, text, (positionX + 15, positionY - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
cv2.imshow('IMAGE', image)

cv2.waitKey(0)
cv2.destroyAllWindows()




