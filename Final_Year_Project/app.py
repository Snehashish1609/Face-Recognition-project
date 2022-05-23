from flask import Flask, render_template, Response
import cv2
import pymongo
import face_recognition
import numpy as np
import user.models as mod
import user.new_image as ni

app = Flask(__name__)

#Database
client = pymongo.MongoClient('localhost', 27017)
db = client.demo

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
known_encodings = mod.face_data().get_fe()
known_names = mod.face_data().get_fn()

def gen_frames():  
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_encodings, face_encoding)
                    name = "Unknown"
                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_names[best_match_index]

                    face_names.append(name)
            #process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#Routes from user import routes
@app.route('/signin')
def signin():
    return render_template('signin.html')
@app.route('/signup_page')
def signup_page():
    return render_template('signup_page.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/signup', methods=['POST'])
def signup():
  return mod.User().signup()
@app.route('/product')
def product():
    return render_template('product.html')
@app.route('/customer')
def customer():
    return render_template('customer.html')
@app.route('/purchase')
def purchase():
    return render_template('purchase.html')
@app.route('/return')
def returnd():
    return render_template('return.html')
@app.route('/result.html')
def Results():
    try:
        rows = db.my_db.find()#.limit(10)
        for row in rows:
            print(row)
        return render_template('results.html', names = row)

    except Exception as e:
        return print("ERROR in RESULTS!!!!!!!!")
if __name__=='__main__':
    app.run(debug=True)
