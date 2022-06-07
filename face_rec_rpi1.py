import face_recognition
import cv2
import numpy as np
from imutils import paths
import random
import time
import threading
from datetime import datetime
import os
os.system("vcgencmd display_power 0")
from gtts import gTTS
import pygame

#from tensorflow.keras.models import load_model
#from tensorflow.keras.preprocessing.image import img_to_array
#from tensorflow.keras.preprocessing import image
# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []
list_image = paths.list_images("known_faces_images/")
for image_path in list_image :
    face_image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(face_image)[0]
    known_face_encodings.append(face_encoding)
    name = image_path.split('/')[-1].split('.')[0]
    known_face_names.append(name)
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
global ret, frame;
ret, frame=None, None;       
def readImageFromCamera():
    global ret, frame, video_capture
    while True:
        ret, frame = video_capture.read()
        
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break        
def visualiseImage():
    global ret, frame, process_this_frame, face_locations, face_encodings, face_names, known_face_encodings, known_face_names
    while True:
        if ret:
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
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        print(name)
                        hour = int(datetime.now().strftime("%H"))
                        print(hour)
                        os.system("vcgencmd display_power 1")
                        if (hour<=10):
                            Morning = ("good morning How was your sleep ", " good morning rise and shine ", "prepare yourself for a new day ", "dont forget to smile and prepare yourself ",  "don't forget to eat before going out ")
                            word = random.choice(Morning)
                            speak=word+name
                            try:                          
                                tts = gTTS(speak,lang = 'en', slow=False)
                                tts.save("hi.mp3")
                                pygame.mixer.init()
                                pygame.mixer.music.load("hi.mp3")
                                pygame.mixer.music.set_volume(1.0)
                                pygame.mixer.music.play()
                                while pygame.mixer.music.get_busy() == True:
                                    pass
                                os.remove("hi.mp3")
                                time.sleep(300)
                            except:                             
                                text = os.system("echo "+word+name+"| festival --tts")
                                time.sleep(300)
                                                              
                        elif (hour>10 and hour<=18):
                            Anytime = ("how are you doing?","i like your smile","i like your body ","you look sexy ","dont forget to pray ", " how was your lunch, did you eat well ? ")
                            word = random.choice(Anytime)
                            speak=word+name
                            try:
                                tts = gTTS(speak,lang = 'en', slow=False)
                                tts.save("hi.mp3")
                                pygame.mixer.init()
                                pygame.mixer.music.load("hi.mp3")
                                pygame.mixer.music.set_volume(1.0)
                                pygame.mixer.music.play()
                                while pygame.mixer.music.get_busy() == True:
                                    pass
                                os.remove("hi.mp3")
                                time.sleep(300)                               
                            except:                               
                                text = os.system("echo "+word+name+ "| festival --tts")
                                time.sleep(300)
                            
                        elif(hour>=19 ):
                            Anytime = ("go to sleep its time for bed  ", "it is late dont forget to go to bed early ","you look tired","dont eat before sleep")
                            word = random.choice(Anytime)
                            speak=word+name
                            try:
                                tts = gTTS(speak,lang = 'en', slow=False)
                                tts.save("hi.mp3")
                                pygame.mixer.init()
                                pygame.mixer.music.load("hi.mp3")
                                pygame.mixer.music.set_volume(1.0)
                                pygame.mixer.music.play()
                                while pygame.mixer.music.get_busy() == True:
                                    pass
                                os.remove("hi.mp3")
                                time.sleep(300)                               
                            except:                               
                                text = os.system("echo "+word+name+ "| festival --tts")
                                time.sleep(300)
                        os.system("vcgencmd display_power 0")                      
                    face_names.append(name)
            process_this_frame = not process_this_frame
threading.Thread(target=readImageFromCamera).start()
#threading.Thread(target=visualiseImage).start()
#threading.Thread(target=saver).start()
visualiseImage()
#saver()
                











