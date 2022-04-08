import cv2
import os

def new_image():
    camera = cv2.VideoCapture(0)
    print("In new_image file!") # check file run status
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # send response to source
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')