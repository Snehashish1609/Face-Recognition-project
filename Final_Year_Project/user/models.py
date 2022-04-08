from flask import Flask, jsonify, request, session, redirect
import uuid
import cv2
import face_recognition
import user.new_image as ni

# face_data contains all the face encoding arrays
class face_data:
    def __init__(self):
        # Load a second sample picture and learn how to recognize it.
        sneh_image = face_recognition.load_image_file("user-image/sneh.jpg")
        sneh_face_encoding = face_recognition.face_encodings(sneh_image)[0]

        idb_image = face_recognition.load_image_file("user-image/IDB.jpg")
        idb_face_encoding = face_recognition.face_encodings(idb_image)[0]

        ani_image = face_recognition.load_image_file("user-image/Ani.jpg")
        ani_face_encoding = face_recognition.face_encodings(ani_image)[0]

        # Create arrays of known face encodings and their names
        self.known_face_encodings = [
          #make this into a dynamic array
          ani_face_encoding,
          sneh_face_encoding,
          idb_face_encoding
        ]
        self.known_face_names = [
            "Anirban",
            "Snehashish",
            "Indra Deb Banerjee"
        ]

    def get_fe(self):
        return self.known_face_encodings

    def get_fn(self):
        return self.known_face_names



from app import db
class User:

  '''def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200'''

  def signup(self):
    print(request.form)

    # Initializing variables
    new_face_locations = []
    new_face_encodings = []
    # get frame from new_image file
    local_frame = ni.NEW_FRAME
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(local_frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    new_face_locations = face_recognition.face_locations(rgb_small_frame)
    new_face_encoding = face_recognition.face_encodings(rgb_small_frame, new_face_locations)

    # Create the user object
    user = {
        #"_id": uuid.uuid4().hex,
        "customerID": "001",
        "name": request.form.get('name'),
        "phone": request.form.get('phone'),
        "address": request.form.get('add'),
        "encoding": new_face_encoding[0].tolist() # -> mongodb can only store lists in the form of arrays
    }

    # Encrypt the password
    #user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # Check for existing email address
    '''if db.users.find_one({ "phone": user['phone'] }):
      return jsonify({ "error": "Phone No. already in use" }), 400'''

    # user details insertion in db
    if db.demos.insert_one(user):
      return redirect('/signin') # self.start_session(user)

    return jsonify({ "error": "Signup failed" }), 400
  
  '''def signout(self):
    session.clear()
    return redirect('/')'''
  
  '''def login(self):

    user = db.users.find_one({
      "phone": request.form.get('phone')
    })

    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
      return self.start_session(user)
    
    return jsonify({ "error": "Invalid login credentials" }), 401'''