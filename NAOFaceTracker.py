#! /usr/bin/env python
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