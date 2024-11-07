import threading
import cv2
import tkinter as tk
from deepface import DeepFace

def get_name():
    name = input("What is your first name ? ")
    return name

def number_of_students():
    try:
        return int(input("How many people should be in attendance ? "))
    except:
        print("Invalid: not a whole integer")
for people in range(number_of_students()):
    my_name = get_name()
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    counter = 0
    face_match = False
    reference = cv2.imread(f"{my_name}.jpg")
    def check_face(frame):
        global face_match
        try:
            if DeepFace.verify(frame, reference.copy())['verified']:
                face_match = True
            else:
                face_match = False
        except ValueError:
            face_match = False
    while True:
        ret, frame = capture.read()
        if ret:
            if counter % 1000 == 0:
                try:
                    threading.Thread(target = check_face, args = (frame.copy(), )).start()
                except ValueError:
                    pass
            counter += 1
            if face_match:
                cv2.putText(frame, "Match", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                print(f"Attendance Recorded: {my_name} is present.")
                break
            else:
                cv2.putText(frame, "No Match", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            cv2.imshow("video", frame) 
        key = cv2.waitKey(1)
        if key == ord("q"):
            exit()
    cv2.destroyAllWindows()






