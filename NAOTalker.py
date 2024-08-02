# -*- coding: UTF-8 -*-
from naoqi import ALProxy

nao_ip = "192.168.1.240"
nao_port = 9559
txtpath = r"D:\plymouth\audioprompt\prompt.txt"


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

def open_response():
    with open(txtpath, 'r') as file:
        my_string = file.read().decode('utf-8')
    print "Response :"
    print my_string
    return my_string

def say_response(response):
    tts2 = ALProxy("ALAnimatedSpeech", nao_ip, nao_port) 
    emotion = "animations/Sit/BodyTalk/BodyTalk_1"
    message = str(response).encode('utf-8')
    tts2.say('^start({emotion}) {message} ^wait({emotion})'.format(emotion=emotion, message=message))

response = open_response()
say_response(response)
