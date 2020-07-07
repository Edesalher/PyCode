import cv2

image = cv2.imread('cartas.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200)

(contours, _) = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image, contours, -1, (0, 0, 255), 2)
print(f'EDGES THAT I FOUND: {len(contours)}')
text = f'EDGES THAT I FOUND: {len(contours)}'

cv2.putText(image, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

cv2.imshow('EDGES', edges)
cv2.imshow('IMAGE', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
