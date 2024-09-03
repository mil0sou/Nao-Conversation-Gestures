# -*- coding: UTF-8 -*-

# ===============================================
#  File       : NAOFaceListener.py
#  Author     : Milo Soulard
#  Python     : 2.7
#  Date       : Summer 2024
#  Description: Detects audio signals
#               Receives face detection from NAOFaceTracker
#               Makes the robot move when listening
#               Starts the recording on the robot
#               Save the audio on the robot's disk
# ===============================================


import sys
from naoqi import ALProxy, ALModule, ALBroker
import time
import threading
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)
conn, addr = server_socket.accept()

IP = "192.168.1.240"
PORT = 9559

myBroker = ALBroker("myBroker", "0.0.0.0", 0, IP, PORT)

facing = False
recording = False
recording_thread = None
listen_duration = 2.0  # seconds avant qu'il s'arrête de record
quitpg = False
audio_path = "/home/nao/audio/prompt.wav"
AUDIO_THRESHOLD = 0.7  # 0 = hearing impaired and 1 = hypersensitive


used_joints = [
    "HeadYaw",
    "HeadPitch",
    "LShoulderPitch",
    "LShoulderRoll",
    "LElbowYaw",
    "LElbowRoll",
    "LWristYaw",
    "RShoulderPitch",
    "RShoulderRoll",
    "RElbowYaw",
    "RElbowRoll",
    "RWristYaw",
    "RHand",
    "LHand",
]

ununsed_joints = [
    "LHipYawPitch",
    "LHipRoll",
    "LHipPitch",
    "LKneePitch",
    "LAnklePitch",
    "LAnkleRoll",
    "RHipYawPitch",
    "RHipRoll",
    "RHipPitch",
    "RKneePitch",
    "RAnklePitch",
    "RAnkleRoll",
]

def round_points(points):
    return [round(p, 2) for p in points]

def update_status():
    global facing, recording
    status = "face : {facing} | recording : {recording}".format(
        facing="TRUE" if facing else "false",
        recording="TRUE" if recording else "false"
    )
    sys.stdout.write("\r" + status)
    sys.stdout.flush()

class SoundDetectionModule(ALModule):
    def __init__(self, name, IP, PORT):
        # initializes
        ALModule.__init__(self, name)
        self.memory = ALProxy("ALMemory", IP, PORT)
        self.memory.subscribeToEvent("SoundDetected", name, "onSoundDetected")
        self.sound_detection = ALProxy("ALSoundDetection", IP, PORT)
        self.sound_detection.setParameter("Sensibility", AUDIO_THRESHOLD)

    #called function when sound is detected
    def onSoundDetected(self, eventName, value, subscriberIdentifier):
        global recording, recording_thread, facing
        print("Sound detected: ", value)
        if not recording: #starts recording and timer 
            if facing: 
                recording = True
                if recording_thread is not None and recording_thread.is_alive():
                    recording_thread.cancel()
                start_recording()
            else:
                print("sound detected but not facing !")
                pass
        else: #restarts timer if sound is detected while recording
            if recording_thread is not None and recording_thread.is_alive():
                recording_thread.cancel()
            recording_thread = threading.Timer(listen_duration, stop_recording) #if timer is over, stops recording 
            recording_thread.start()


def start_recording():
    global recording, recording_thread
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    tts.say("Hi!") # if sound is detected 
    audio_recorder = ALProxy("ALAudioRecorder", IP, PORT)
    audio_recorder.stopMicrophonesRecording()
    audio_recorder.startMicrophonesRecording(audio_path, "wav", 16000, [0, 0, 1, 0])
    print("Recording started.")


def stop_recording():
    global recording, myBroker, quitpg
    audio_recorder = ALProxy("ALAudioRecorder", IP, PORT)
    audio_recorder.stopMicrophonesRecording()
    print("Recording stopped.")
    recording = False
    quitpg = True
    SoundDetection.memory.unsubscribeToEvent("SoundDetected", "SoundDetection")
    myBroker.shutdown()
    sys.exit(0)


def main(IP, PORT=9559):
    global SoundDetection, recording, myBroker, facing
    
    basic_awareness = ALProxy("ALBasicAwareness", IP, PORT)
    motion = ALProxy("ALMotion", IP, PORT)

    for joint in used_joints:
        motion.setStiffnesses(joint, 1.0)
        # motion.setAngles(joint, 0, 0.5)

    for joint in ununsed_joints:
        motion.setStiffnesses(joint, 1.0)
        # motion.setAngles(joint, 0, 0.5)

    motion.wakeUp() #robot will track your face
    
    basic_awareness.startAwareness()
    """postureProxy = ALProxy("ALRobotPosture", IP, PORT)
    postureProxy.goToPosture("Sit", 1.0)"""
    time.sleep(0.05)
    SoundDetection = SoundDetectionModule("SoundDetection", IP, PORT)
    try:
        while not quitpg:
            time.sleep(0.05)
            data = conn.recv(1024)
            facing = "1" in data
            #update_status()






            #print("face detected:", data)
            # facing = data == "1" #str to bool
             #
            if recording:
                #print("Recording...")
                pass
            else:
                #print("Waiting for sound...")
                pass

    except quitpg:
        #print("Interrupted by user, shutting down")
        SoundDetection.memory.unsubscribeToEvent("SoundDetected", "SoundDetection")
        myBroker.shutdown()
        conn.close()
        server_socket.close()
        sys.exit(0)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main(IP, PORT)
    
    
