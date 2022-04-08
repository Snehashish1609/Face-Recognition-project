import os
import face_recognition

def new_image_encoding():
    nimage = face_recognition.load_image_file("user-image/image_0.jpg")
    image_encodings = face_recognition.face_encodings(nimage)[0]

    print(image_encodings)

    os.remove("user-image/image_0.jpg")

    return image_encodings