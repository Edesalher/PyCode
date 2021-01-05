import cv2

# To capture video from the camera or read a video file.
capture = cv2.VideoCapture(0)
# capture = cv2.VideoCapture('record.avi')

# To save a video.
# Define the codec and create VideoWriter object
# out = cv2.VideoWriter('record.avi', cv2.VideoWriter_fourcc(*'XVID'), 30.0, (640, 480))

while capture.isOpened():
    # Capture frame-by-frame.
    ret, frame = capture.read()
    if ret:
        # Displaying the frame.
        cv2.imshow('CAMERA', frame)
        # Writing the frame.
        # out.write(frame)
        if cv2.waitKey(30) & 0xFF == ord('e'):  # Press 'e' to exit.
            break
    else:
        break

# When everything done, release the capture an so on.
capture.release()
# out.release()
cv2.destroyAllWindows()
