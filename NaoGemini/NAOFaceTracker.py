# -*- coding: UTF-8 -*-

# ===============================================
#  File       : NAOFaceTracker.py
#  Author     : Milo Soulard
#  Python     : 2.7
#  Date       : Summer 2024
#  Description: Detects if user is facing and near the robot
#               Sends it to NAOFaceListener
# ===============================================

import time, socket
from naoqi import ALProxy

IP = "192.168.1.240"
PORT = 9559
facing = False
near = False
FACING_THRESHOLD = 0.07  # 0 pareidolie  1 aveugle
DISTANCE_TRESHOLD = 2.0
#tts = ALProxy("ALTextToSpeech", IP, PORT)

basic_awareness = ALProxy("ALBasicAwareness", IP, PORT)
motion = ALProxy("ALMotion", IP, PORT)
motion.wakeUp()
basic_awareness.startAwareness()
faceProxy = ALProxy("ALFaceDetection", IP, PORT)
faceProxy.subscribe("Test_Face", 100, 0.0 )
memValue = "FaceDetected"
memoryProxy = ALProxy("ALMemory", IP, PORT)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))


def round_points(points):
    return [round(p, 2) for p in points]

def checkface(val):
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
                    #print(diffdg1,diffdg2)
                    facing1= diffdg1 > FACING_THRESHOLD
                    facing2= diffdg2 > FACING_THRESHOLD
                    if facing1 or facing2:
                        
                        total_sum=0
                        for left, right in zip(leftEyePoints, rightEyePoints):
                            total_sum += abs(left) + abs(right)
                        print(total_sum)
                        if total_sum < DISTANCE_TRESHOLD:
                            print("VISAGE DE FACE !!")
                            print(leftEyePoints[:6] ,rightEyePoints[:6])
                            facing = True
                        else:
                            print("visage de face mais trop loin ")
                            facing = False
                        #tts.say("Hi!")
                    else:
                       print("visage detecte mais pas de face")
                       facing = False
                else:
                    print("visage semi visible ")
                    facing = False
   
    else:
        print("Aucun visage detecte")
        facing = False
    return facing

def checknear(val):
    if val and isinstance(val, list) and len(val) >= 2:
        faceInfoArray = val[1]
        for faceInfo in faceInfoArray:
            if isinstance(faceInfo, list) and len(faceInfo) >= 2:
                extraInfo = faceInfo[1]
                leftEyePoints = round_points(extraInfo[3])
                rightEyePoints = round_points(extraInfo[4]) 
                if "truc":
                    near = True
                else:
                    near = False
    else:
        near = False
    return near


while True:
    #time.sleep(0.05)
    val = memoryProxy.getData(memValue)
    facing = checkface(val)
    near = checknear(val)
    facingstr = "1" if facing else "0"

    client_socket.sendall(facingstr.encode())



'''# -*- coding: utf-8 -*-
import sys, threading
from naoqi import ALProxy, ALModule, ALBroker
import socket

nao_ip = "192.168.1.240"
nao_port = 9559

"""client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))"""

IP = "192.168.1.240"
PORT = 9559
facing = False
FACING_THRESHOLD = 0.0065  # 0 pareidolie  1 aveugle


class FaceDetectionModule(ALModule):
    def __init__(self, IP, PORT):
        ALModule.__init__(self, "FaceDetectionModule")
        self.memoryProxy = ALProxy("ALMemory", IP, PORT)

    def round_points(self, points):
        return [round(p, 2) for p in points]

    def process_faces(self):
        global facing
        memValue = "FaceDetected"
        val = self.memoryProxy.getData(memValue)
        if val and isinstance(val, list) and len(val) >= 2:
            faceInfoArray = val[1]
            for faceInfo in faceInfoArray:
                if isinstance(faceInfo, list) and len(faceInfo) >= 2:
                    extraInfo = faceInfo[1]
                    leftEyePoints = self.round_points(extraInfo[3])
                    rightEyePoints = self.round_points(extraInfo[4])
                    if leftEyePoints != rightEyePoints:
                        diffdg1 = round(abs((leftEyePoints[0] - rightEyePoints[0])), 2)
                        diffdg2 = round(abs((rightEyePoints[0] - leftEyePoints[0])), 2)
                        print(diffdg1, diffdg2)
                        facing1 = diffdg1 > FACING_THRESHOLD
                        facing2 = diffdg2 > FACING_THRESHOLD
                        if facing1 or facing2:
                            print("VISAGE DE FACE !!")
                            facing = True
                        else:
                            print("visage detecte mais pas de face")
                            facing = False
                    else:
                        print("visage semi visible ")
                        facing = False
        else:
            #print("Aucun visage detecte")
            facing = False
    
    facingstr = "1" if facing else "0"
    print(facingstr)
    #client_socket.sendall(facingstr.encode())

class MotionControlModule:
    def __init__(self, IP, PORT):
        self.motion = ALProxy("ALMotion", IP, PORT)
        self.basic_awareness = ALProxy("ALBasicAwareness", IP, PORT)
        self.used_joints = [
            "HeadYaw", "HeadPitch", "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
            "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand", "LHand"
        ]
        self.unused_joints = [
            "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll",
            "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll"
        ]
        self.init_motion()

    def init_motion(self):
        for joint in self.used_joints:
            self.motion.setStiffnesses(joint, 1.0)
        for joint in self.unused_joints:
            self.motion.setStiffnesses(joint, 0.0)
        self.motion.wakeUp()
        self.basic_awareness.startAwareness()

class NaoRobot:
    def __init__(self, IP, PORT):
        self.broker = ALBroker("myBroker", "0.0.0.0", 0, IP, PORT)
        self.face_detection_module = FaceDetectionModule(IP, PORT)
        self.motion_control_module = MotionControlModule(IP, PORT)

    def run(self):
        global facing
        try:
            while True:
                self.face_detection_module.process_faces()
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        print("Shutting down...")
        self.broker.shutdown()
        sys.exit(0)


def main():
    nao_robot = NaoRobot(IP, PORT)
    nao_robot.run()

if __name__ == "__main__":
    main()
'''