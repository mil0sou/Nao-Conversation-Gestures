# -*- coding: UTF-8 -*-

# ===============================================
#  File       : NAOTalker.py
#  Author     : Milo Soulard
#  Python     : 2.7
#  Date       : Summer 2024
#  Description: Receives the response from gemini and makes the robot talk
# ===============================================

from naoqi import ALProxy
import time

nao_ip = "192.168.1.240"
nao_port = 9559
txtpath = r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\prompt.txt"


motionProxy = ALProxy("ALMotion", nao_ip, nao_port)
#used_joints = ["RShoulderRoll", "RShoulderPitch", "RElbowYaw", "RElbowRoll","LShoulderRoll", "LShoulderPitch", "LElbowYaw", "LElbowRoll"]
used_joints = ["HeadYaw","HeadPitch","LShoulderPitch","LShoulderRoll",  "LElbowYaw","LElbowRoll","LWristYaw","RShoulderPitch","RShoulderRoll","RElbowYaw","RElbowRoll","RWristYaw","RHand","LHand"]
ununsed_joints = ["LHipYawPitch","LHipRoll","LHipPitch" ,"LKneePitch","LAnklePitch","LAnkleRoll","RHipYawPitch","RHipRoll","RHipPitch","RKneePitch","RAnklePitch","RAnkleRoll",]

for joint in used_joints:    # moving parts 
    motionProxy.setStiffnesses(joint, 1.0) 
    #motionProxy.setAngles(joint, 0, 0.5)

for joint in ununsed_joints: # not moving parts 
    motionProxy.setStiffnesses(joint, 0.0) 
    #motionProxy.setAngles(joint, 0, 0.5)

def open_response():    #open the txt file and get the response from the LLM
    with open(txtpath, 'r') as file:
        my_string = file.read().decode('utf-8')
    print("Response :")
    print(my_string)
    return my_string


def say_response(response):
    tts = ALProxy("ALAnimatedSpeech", nao_ip, nao_port) 
    emotion = "animations/Sit/BodyTalk/BodyTalk_1" #speaks with an animation
    message = str(response).encode('utf-8')
    """for joint in ununsed_joints: # not moving parts 
        motionProxy.setStiffnesses(joint, 0.0)"""
    tts.say('^start({emotion}) {message} ^wait({emotion})'.format(emotion=emotion, message=message))
    time.sleep(0.5)

response = open_response()
say_response(response)
