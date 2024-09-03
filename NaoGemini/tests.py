# -*- coding: UTF-8 -*-
import time
from naoqi import ALProxy
import matplotlib.pyplot as plt

IP = "192.168.1.240"
PORT = 9559
near = False

faceProxy = ALProxy("ALFaceDetection", IP, PORT)
faceProxy.subscribe("Test_Face", 500, 0.0)
memValue = "FaceDetected"
memoryProxy = ALProxy("ALMemory", IP, PORT)

def round_points(points):
    return [round(p, 2) for p in points]

def checknear(val):
    global near  
    if val and isinstance(val, list) and len(val) >= 2:
        faceInfoArray = val[1]
        for faceInfo in faceInfoArray:
            if isinstance(faceInfo, list) and len(faceInfo) >= 2:
                extraInfo = faceInfo[1]
                leftEyePoints = round_points(extraInfo[3])
                rightEyePoints = round_points(extraInfo[4])
                print(leftEyePoints[:6] ,rightEyePoints[:6])
                print
                total_sum=0
                for left, right in zip(leftEyePoints, rightEyePoints):
                    total_sum += abs(left) + abs(right)
                print(total_sum)
                if "truc":
                    near = True
                else:
                    near = False
    else:
        #print("no face")
        near = False
    return near

left_eye_history = [[] for _ in range(6)]
right_eye_history = [[] for _ in range(6)]
x_values = [] 

def update_plots(ax, leftEyePoints, rightEyePoints, step):
    x_values.append(step)

    for i in range(6):
        left_eye_history[i].append(leftEyePoints[i])
        right_eye_history[i].append(rightEyePoints[i])
        
        ax[i].cla() 
        ax[i].plot(x_values, left_eye_history[i], marker='o', color='b', label='Left Eye')
        ax[i].plot(x_values, right_eye_history[i], marker='o', color='r', label='Right Eye')
        
        ax[i].set_xlim(0, max(x_values)) 
        ax[i].set_ylim(-1, 1)
        ax[i].legend(loc='upper right')
        ax[i].set_title('Point {}'.format(i + 1))


def main():
    fig, ax = plt.subplots(2, 6, figsize=(15, 5))
    ax = ax.ravel()  
    step = 0  # Initialisation de l'étape
    while True:
        #for i in range(0,30):
        time.sleep(0.1)
        val = memoryProxy.getData(memValue)
        near = checknear(val)

        if val and isinstance(val, list) and len(val) >= 2:
            faceInfoArray = val[1]
            for faceInfo in faceInfoArray:
                if isinstance(faceInfo, list) and len(faceInfo) >= 2:
                    extraInfo = faceInfo[1]
                    leftEyePoints = round_points(extraInfo[3])
                    rightEyePoints = round_points(extraInfo[4])
                    #update_plots(ax, leftEyePoints, rightEyePoints, step)
                    step += 1  # Incrémenter l'étape
        #plt.show()

if __name__ == "__main__":
    main()




'''import time, socket
from naoqi import ALProxy

IP = "192.168.1.240"
PORT = 9559
near = False


faceProxy = ALProxy("ALFaceDetection", IP, PORT)
faceProxy.subscribe("Test_Face", 500, 0.0 )
memValue = "FaceDetected"
memoryProxy = ALProxy("ALMemory", IP, PORT)

def round_points(points):
    return [round(p, 2) for p in points]

def checknear(val):
    if val and isinstance(val, list) and len(val) >= 2:
        faceInfoArray = val[1]
        for faceInfo in faceInfoArray:
            if isinstance(faceInfo, list) and len(faceInfo) >= 2:
                extraInfo = faceInfo[1]
                leftEyePoints = round_points(extraInfo[3])
                rightEyePoints = round_points(extraInfo[4]) 
                print(leftEyePoints[:6])
                print(rightEyePoints[:6])
                print
                if "truc":
                    near = True
                else:
                    near = False
    else:
        print("no face")
        near = False
    return near

def main():
    while True:
        time.sleep(0.05)
        val = memoryProxy.getData(memValue)
        near = checknear(val)

main()'''




#different drafts and tests
'''import subprocess
python27path = r"C:\Python27\python.exe"
python312path = r"C:\Users\soula\AppData\Local\Microsoft\WindowsApps\python3.exe"

def runListener():
    subprocess.run([python27path, r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\NAOListener.py"])

def runThinker():
    subprocess.run([python312path, r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\NAOThinker.py"])

def runTalker():
    subprocess.run([python27path, r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\NAOTalker.py"])

def main():
    while True:
        runListener()   
        runThinker()
        runTalker()

if __name__ == "__main__":
    main()'''
    
    
'''import subprocess
import threading

python27path = r"C:\Python27\python.exe"
python312path = r"C:\Users\soula\AppData\Local\Microsoft\WindowsApps\python3.exe"

def runListener():
    subprocess.run([python27path, r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\NAOFaceListener.py"])

def runTracker():
    subprocess.run([python27path, r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\NAOFaceTracker.py"])

def runThinker():
    subprocess.run([python312path, r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\NAOThinker.py"])

def runTalker():
    subprocess.run([python27path, r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\NAOTalker.py"])

def main():
    while True:
        listener1_thread = threading.Thread(target=runListener)
        listener2_thread = threading.Thread(target=runTracker)
        
        listener1_thread.start()
        listener2_thread.start()
        
        while listener1_thread.is_alive() and listener2_thread.is_alive():
            listener1_thread.join(timeout=1)
            listener2_thread.join(timeout=1)
        
        runThinker()
        runTalker()

if __name__ == "__main__":
    main()'''



"""#!/usr/bin/env python
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
    run()"""


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

'''#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
                    
#print("Points de l'oeil gauche:", leftEyePoints[:6])
#print("Points de l'oeil droit:", rightEyePoints[:6])
#print("Points du nez:", nosePoints)
"""
EyePoints =
[
eyeCenter_x,
eyeCenter_y,
noseSideLimit_x,
noseSideLimit_y,
earSideLimit_x,
earSideLimit_y,
topLimit_x,
topLimit_y,
bottomLimit_x,
bottomLimit_y,
midTopEarLimit_x,
midTopEarLimit_y,
midTopNoseLimit_x,
midTopNoseLimit_y
]
"""
import time
from naoqi import ALProxy

IP = "192.168.1.240"
PORT = 9559
FACING_THRESHOLD = 0.07 

tts = ALProxy("ALTextToSpeech", IP, PORT)

basic_awareness = ALProxy("ALBasicAwareness", IP, PORT)
motion = ALProxy("ALMotion", IP, PORT)
motion.wakeUp()
basic_awareness.startAwareness()


faceProxy = ALProxy("ALFaceDetection", IP, PORT)
period = 500
faceProxy.subscribe("Test_Face", period, 0.0 )
memValue = "FaceDetected"
memoryProxy = ALProxy("ALMemory", IP, PORT)

def round_points(points):
    return [round(p, 2) for p in points]


while True:
    time.sleep(0.1)
    print("") 
    
    val = memoryProxy.getData(memValue)
    if val and isinstance(val, list) and len(val) >= 2:
        faceInfoArray = val[1]
        for faceInfo in faceInfoArray:
            if isinstance(faceInfo, list) and len(faceInfo) >= 2:
                extraInfo = faceInfo[1]
                leftEyePoints = round_points(extraInfo[3])
                rightEyePoints = round_points(extraInfo[4]) 
                if leftEyePoints != rightEyePoints:
                    diffdg1 = round(abs((leftEyePoints[0] - rightEyePoints[0])),2)
                    diffdg2 = round(abs((rightEyePoints[0] - leftEyePoints[0])),2)
                    print(diffdg1,diffdg2)
                    facing1= diffdg1 > FACING_THRESHOLD
                    facing2= diffdg2 > FACING_THRESHOLD
                    if facing1 or facing2:
                        print("VISAGE DE FACE !!")
                        tts.say("Hi!")
                    else:
                       print("visage detecte mais pas de face")
                else:
                    print("visage semi visible ")
   
    else:
        print("Aucun visage detecte")




'''



'''while True:
  time.sleep(0.5)
  val = memoryProxy.getData(memValue)

  if(val and isinstance(val, list) and len(val) >= 2):
    timeStamp = val[0]
    faceInfoArray = val[1]

    try:
      for j in range( len(faceInfoArray)-1 ):
        faceShapeInfo = faceInfo[0]
        faceExtraInfo = faceInfo[1]

        print "  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])
        print "  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])

    except Exception, e:
      print "faces detected, but it seems getData is invalid. ALValue ="
      print val
      print "Error msg %s" % (str(e))
  else:
    print "No face detected"'''



'''import qi
import argparse
import sys


def main(session):
    """
    When tracking is activated, faces looking sideways, or located further away
    should be tracked for a longer period.
    Launch Monitor, Camera-Viewer, activate face detection, and see if it works better.
    """

    tracking_enabled = True

    # Get the service ALFaceDetection.

    face_service = session.service("ALFaceDetection")

    print "Will set tracking to '%s' on the robot ..." % tracking_enabled

    # Enable or disable tracking.
    face_service.enableTracking(tracking_enabled)

    # Just to make sure correct option is set.
    print "Is tracking now enabled on the robot?", face_service.isTrackingEnabled()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.240",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)'''



'''# -*- encoding: UTF-8 -*-


from naoqi import ALProxy
import sys
nao_ip = "192.168.1.240"
nao_port = 9559

motionProxy = ALProxy("ALMotion", nao_ip, nao_port)
#used_joints = ["RShoulderRoll", "RShoulderPitch", "RElbowYaw", "RElbowRoll","LShoulderRoll", "LShoulderPitch", "LElbowYaw", "LElbowRoll"]
used_joints = ["HeadYaw","HeadPitch","LShoulderPitch","LShoulderRoll",  "LElbowYaw","LElbowRoll","LWristYaw","RShoulderPitch","RShoulderRoll","RElbowYaw","RElbowRoll","RWristYaw","RHand","LHand"]
ununsed_joints = ["LHipYawPitch","LHipRoll","LHipPitch" ,"LKneePitch","LAnklePitch","LAnkleRoll","RHipYawPitch","RHipRoll","RHipPitch","RKneePitch","RAnklePitch","RAnkleRoll",]
for joint in used_joints:
    motionProxy.setStiffnesses(joint, 1.0)
    motionProxy.setAngles(joint, 0, 0.5)

for joint in ununsed_joints:
    motionProxy.setStiffnesses(joint, 0.0)
    motionProxy.setAngles(joint, 0, 0.5)

USAGE = "USAGE:\n" \
        "python vision_setfacetracking.py [NAO_IP] [0 or 1] \n" \
        "\nExamples: \n" \
        "Enable tracking: set_tracking.py 192.168.1.102 1\n" \
        "Disable tracking: set_tracking.py 192.168.1.102 0"


def set_nao_face_detection_tracking(nao_ip, nao_port, tracking_enabled):
    """Make a proxy to nao's ALFaceDetection and enable/disable tracking.

    """
    faceProxy = ALProxy("ALFaceDetection", nao_ip, nao_port)

    print "Will set tracking to '%s' on the robot ..." % tracking_enabled

    # Enable or disable tracking.
    faceProxy.enableTracking(tracking_enabled)

    # Just to make sure correct option is set.
    print "Is tracking now enabled on the robot?", faceProxy.isTrackingEnabled()


def main():
    # Specify your IP address here.


    tracking_enabled = True

    set_nao_face_detection_tracking(nao_ip, nao_port, tracking_enabled)




if __name__ == "__main__":
    main()

'''

'''
import sys
from naoqi import ALProxy



class SoundDetectionModule(ALModule):
    def __init__(self, name, IP, PORT):
        ALModule.__init__(self, name)
        self.memory = ALProxy("ALMemory", IP, PORT)
        self.sound_detection = ALProxy("ALSoundDetection", IP, PORT)
        self.sound_detection.setParameter("Sensibility", 0.8) # 0 sourd 1 hypersensible 
        self.memory.subscribeToEvent("SoundDetected", name, "onSoundDetected")
    
    def onSoundDetected(self, eventName, value, subscriberIdentifier):
        global recording, recording_thread
        #print("Sound detected: ", value)
        if not recording:
            recording = True
            if recording_thread is not None and recording_thread.is_alive():
                recording_thread.cancel()
            start_recording()
        else:
            if recording_thread is not None and recording_thread.is_alive():
                recording_thread.cancel()
            recording_thread = threading.Timer(listen_duration, stop_recording)
            recording_thread.start()

def start_recording():
    global recording, recording_thread


    audio_path = "/home/nao/audio/prompt.wav"
    audio_recorder = ALProxy("ALAudioRecorder", nao_ip, nao_port)
    audio_recorder.stopMicrophonesRecording()
    audio_recorder.startMicrophonesRecording(audio_path, "wav", 16000, [0, 0, 1, 0])
    print("Recording started.")

def stop_recording():
    global recording, myBroker, quitpg
    audio_recorder = ALProxy("ALAudioRecorder", nao_ip, nao_port)
    audio_recorder.stopMicrophonesRecording()
    print("Recording stopped.")
    recording = False
    quitpg = True
    SoundDetection.memory.unsubscribeToEvent("SoundDetected", "SoundDetection")
    myBroker.shutdown()
    sys.exit(0)


def main(IP, PORT=9559):
    
    global SoundDetection,recording, myBroker
    SoundDetection = SoundDetectionModule("SoundDetection", IP, PORT)
    
    try:
        while not quitpg:
            time.sleep(1)
            if recording:
                print("Recording...")
            else:
                print("Waiting for sound...")
    except quitpg:
        print("Interrupted by user, shutting down")
        SoundDetection.memory.unsubscribeToEvent("SoundDetected", "SoundDetection")
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main(nao_ip, nao_port)'''