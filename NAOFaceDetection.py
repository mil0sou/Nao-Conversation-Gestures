#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import time
import sys

IP = "192.168.1.240"
PORT = 9559
ALPHA_THRESHOLD = 0.1  
BETA_THRESHOLD = 0.1  

def on_human_tracked(value):
    sys.stdout.write("\r")  
    if value == []:
        sys.stdout.write("No face detected       ")
    else:
        faceInfoArray = value[1]
        for j in range(len(faceInfoArray) - 1):
            faceInfo = faceInfoArray[j]
            faceShapeInfo = faceInfo[0]
            alpha = faceShapeInfo[1]
            beta = faceShapeInfo[2]
            width = faceShapeInfo[3]
            height = faceShapeInfo[4]
            
            sys.stdout.write("Alpha: %.3f, Beta: %.3f, Width: %.3f, Height: %.3f" % (alpha, beta, width, height))
            if abs(alpha) < ALPHA_THRESHOLD and abs(beta) < BETA_THRESHOLD:
                sys.stdout.write(", Face is facing the robot      ")
            else:
                sys.stdout.write(", Face is not facing the robot      ")
    sys.stdout.flush()

def run():
    connection_url = "tcp://" + IP + ":" + str(PORT)
    app = qi.Application(["FaceDetection", "--qi-url=" + connection_url])
    
    try:
        app.start()
    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + IP + "\" on port " + str(PORT) + "\".\n"
              "Please check your script arguments.")
        sys.exit(1)

    session = app.session
    memory = session.service("ALMemory")
    subscriber = memory.subscriber("FaceDetected")
    subscriber.signal.connect(on_human_tracked)
    face_detection = session.service("ALFaceDetection")
    face_detection.subscribe("HumanGreeter")

    #print("Starting face detection")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user, stopping face detection")
        face_detection.unsubscribe("HumanGreeter")
        sys.exit(0)

if __name__ == "__main__":
    run()


"""#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import time
import sys

IP = "192.168.1.240"
PORT = 9559

def on_human_tracked(value):
    sys.stdout.flush()
    if value == []:   #no
        sys.stdout.write("\rNo Face detected         ")    
    else:             #ace
        sys.stdout.write("\rFace detected         ")            
    

def run():
    connection_url = "tcp://" + IP + ":" + str(PORT)
    app = qi.Application(["FaceDetection", "--qi-url=" + connection_url])
    
    try:
        app.start()
    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + IP + "\" on port " + str(PORT) + "\".\n"
              "Please check your script arguments.")
        sys.exit(1)

    session = app.session
    memory = session.service("ALMemory")
    subscriber = memory.subscriber("FaceDetected")
    subscriber.signal.connect(on_human_tracked)
    face_detection = session.service("ALFaceDetection")
    face_detection.subscribe("HumanGreeter")

    print("Starting face detection")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user, stopping face detection")
        face_detection.unsubscribe("HumanGreeter")
        sys.exit(0)

if __name__ == "__main__":
    run()
"""



"""#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import time
import sys
import argparse


class HumanGreeter(object):
    def __init__(self, app):
        super(HumanGreeter, self).__init__()
        app.start()
        session = app.session
        self.memory = session.service("ALMemory")
        self.subscriber = self.memory.subscriber("FaceDetected")
        self.subscriber.signal.connect(self.on_human_tracked)
        self.tts = session.service("ALTextToSpeech")
        self.face_detection = session.service("ALFaceDetection")
        self.face_detection.subscribe("HumanGreeter")
        self.got_face = False

    def on_human_tracked(self, value):
        if value == []:  
            self.got_face = False
        elif not self.got_face: 
            self.got_face = True
            print "I saw a face!"
            self.tts.say("Hello, you!")
            # First Field = TimeStamp.
            timeStamp = value[0]
            print "TimeStamp is: " + str(timeStamp)
            faceInfoArray = value[1]
            for j in range( len(faceInfoArray)-1 ):
                faceInfo = faceInfoArray[j]
                faceShapeInfo = faceInfo[0]
                faceExtraInfo = faceInfo[1]
                print "Face Infos :  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])
                print "Face Infos :  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])
                print "Face Extra Infos :" + str(faceExtraInfo)

    def run(self):
        print "Starting HumanGreeter"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping HumanGreeter"
            self.face_detection.unsubscribe("HumanGreeter")
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.240",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["HumanGreeter", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    human_greeter = HumanGreeter(app)
    human_greeter.run()"""