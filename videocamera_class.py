import cv2
import copy
import numpy as np
# from imutils.video import WebcamVideoStream
from imutils.video import VideoStream
import time

import face_recognition



class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = VideoStream(src=0).start()
        # time.sleep(2.0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.stop()

    def get_frame(self):
        image = self.video.read()
        print(type(image))

        # Detect face in image and show a bounding around face if detected, if face not detected then pass the frame normally as it is.
        frame = copy.deepcopy(image)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        faces = face_cascade.detectMultiScale(gray, 1.3, 4)
        for (x,y,w,h) in faces:
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        # face_locations = face_recognition.face_locations(frame)
        # if len(face_locations) == 0:
        #     pass
        # else:
        #     if len(face_locations) == 1:
        #         (top, right, bottom, left) = face_locations[0]
        #         cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        #     else:
        #         for each_face in face_locations:
        #             (top, right, bottom, left) = each_face[0]
        #             frame = cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', frame)
        return (image, jpeg.tobytes())