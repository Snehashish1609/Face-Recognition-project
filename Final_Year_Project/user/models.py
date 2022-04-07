from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
import uuid
import face_recognition
import pymongo
import numpy as np

#Database
client = pymongo.MongoClient('localhost', 27017)
db = client.my_db

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

        # fetch encodings from mongodb
        '''self.known_face_encodings = []
        en = db.my_db.find({}, { 'encoding' :1, '_id' :0})
        for i in en:
            self.known_face_encodings.append(np.fromstring(i['encoding'], dtype=float, count=-1, sep=' '))
        print(self.known_face_encodings) #unsuccessful type conversion <-- to see'''

        # fetching names from mongodb
        self.known_face_names = []
        nm = db.my_db.find({}, { 'name' :1, '_id' :0})
        for j in nm:
            self.known_face_names.append(j['name'])
        print(self.known_face_names) #printing array successfully

        # Create arrays of known face encodings and their names
        self.known_face_encodings = [
          #make this into a dynamic array
          ani_face_encoding,
          sneh_face_encoding,
          idb_face_encoding
        ]

    def get_fe(self):
        return self.known_face_encodings

    def get_fn(self):
        return self.known_face_names



class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  def signup(self):
    print(request.form)

    # Create the user object
    user = {
        "_id": uuid.uuid4().hex,
        "customerID": request.form.get('id'),
        "name": request.form.get('name'),
        "phone": request.form.get('phone'),
        "address": request.form.get('add')
    }

    # Encrypt the password
    #user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # Check for existing email address
    if db.users.find_one({ "phone": user['phone'] }):
      return jsonify({ "error": "Phone No. already in use" }), 400

    if db.users.insert_one(user):
      return self.start_session(user)

    return jsonify({ "error": "Signup failed" }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  '''def login(self):

    user = db.users.find_one({
      "phone": request.form.get('phone')
    })

    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
      return self.start_session(user)
    
    return jsonify({ "error": "Invalid login credentials" }), 401'''