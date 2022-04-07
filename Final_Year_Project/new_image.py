import cv2
import os

def new_image():
    lower = r'D:\code\Face-Recognition-project\Final_Year_Project\user-image'
    upper = r'D:\code\Face-Recognition-project\Final_Year_Project'

    cam = cv2.VideoCapture(0)
    #cv2.namedWindow("test")

    def image_counter():
        f = open("image_number.txt", "r")
        img_counter = int(f.readline())
        print(img_counter)
        f.close()
        return img_counter

    img_counter = image_counter()


    while True:
        os.chdir(lower)
        frame = cam.read()
        '''ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)'''

        k = cv2.waitKey(1)
        if k%256 == 27:
            os.chdir(upper)
            fw = open("image_number.txt", "w")
            fw.write(str(img_counter))
            fw.close()
            print("Escape hit, closing...")
            break

        elif k%256 == 32:
            img_name = "image_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
    
        buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
