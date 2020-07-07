import cv2
import sys

window_name = 'CAMERA'
capture = cv2.VideoCapture('record.avi')
# video = cv2.VideoWriter('record.avi', cv2.VideoWriter_fourcc(*'XVID'), 30.0, (640, 480))

while capture.isOpened():
    ret, image = capture.read()
    if ret:
        cv2.imshow(window_name, image)
#        video.write(image)
        if cv2.waitKey(30) & 0xFF == ord('e'):  # Press 'e' to exit.
            break
    else:
        break

capture.release()
# video.release()
cv2.destroyAllWindows()
