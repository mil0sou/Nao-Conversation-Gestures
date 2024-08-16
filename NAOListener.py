# -*- coding: utf-8 -*-
import sys, time, threading
from naoqi import ALProxy, ALModule, ALBroker

IP = "192.168.1.240"
PORT = 9559
facing = False
FACING_THRESHOLD = 0.065  # 0 pareidolie  1 aveugle
AUDIO_THRESHOLD = 0.7  # 0 sourd 1 hypersensible


class SoundDetectionModule(ALModule):
    def __init__(self, name, IP, PORT):
        ALModule.__init__(self, name)
        self.name = name
        self.memory = ALProxy("ALMemory", IP, PORT)
        self.sound_detection = ALProxy("ALSoundDetection", IP, PORT)
        self.sound_detection.setParameter("Sensibility", AUDIO_THRESHOLD)
        self.faceProxy = ALProxy("ALFaceDetection", IP, PORT)
        self.faceProxy.subscribe("Test_Face", 500, 0.0)
        #print("name :", name, type(name))
        self.memory.subscribeToEvent("SoundDetected", self.name , "onSoundDetected")
        self.recording = False
        self.recording_thread = None
        self.listen_duration = 2


    def onSoundDetected(self, eventName, value):
        global facing
        print("Sound detected: ", value)
        if facing: 
            if not self.recording:
                self.recording = True
                if self.recording_thread is not None and self.recording_thread.is_alive():
                    self.recording_thread.cancel()
                self.start_recording()
            else:
                if self.recording_thread is not None and self.recording_thread.is_alive():
                    self.recording_thread.cancel()
                self.recording_thread = threading.Timer(self.listen_duration, self.stop_recording)
                self.recording_thread.start()
        else:
            print("pas facing, ignored")

    def start_recording(self):
        print("Starting recording...")
        tts = ALProxy("ALTextToSpeech", IP, PORT)
        tts.say("Hi!")
        audio_path = "/home/nao/audio/prompt.wav"
        audio_recorder = ALProxy("ALAudioRecorder", IP, PORT)
        audio_recorder.stopMicrophonesRecording()
        audio_recorder.startMicrophonesRecording(audio_path, "wav", 16000, [0, 0, 1, 0])

    def stop_recording(self):
        print("Stopping recording...")
        audio_recorder = ALProxy("ALAudioRecorder", IP, PORT)
        audio_recorder.stopMicrophonesRecording()
        self.recording = False


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
                        #print(diffdg1, diffdg2)
                        facing1 = diffdg1 > FACING_THRESHOLD
                        facing2 = diffdg2 > FACING_THRESHOLD
                        if facing1 or facing2:
                            #print("VISAGE DE FACE !!")
                            facing = True
                        else:
                            #print("visage detecte mais pas de face")
                            facing = False
                    else:
                        #print("visage semi visible ")
                        facing = False
        else:
            #print("Aucun visage detecte")
            facing = False

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
        self.sound_detection_module = SoundDetectionModule("onSoundDetected", IP, PORT)
        self.face_detection_module = FaceDetectionModule(IP, PORT)
        self.motion_control_module = MotionControlModule(IP, PORT)

    def run(self):
        global facing
        try:
            while True:
                time.sleep(0.1)
                self.face_detection_module.process_faces()
                #print("Facing: ", facing)
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        print("Shutting down...")
        self.sound_detection_module.memory.unsubscribeToEvent("SoundDetected", "SoundDetection")
        self.broker.shutdown()
        sys.exit(0)


def main():
    nao_robot = NaoRobot(IP, PORT)
    nao_robot.run()

if __name__ == "__main__":
    main()

"""import sys
from naoqi import ALProxy, ALModule, ALBroker
import time
import threading

IP = "192.168.1.240"
PORT = 9559

myBroker = ALBroker("myBroker", "0.0.0.0", 0, IP, PORT)

facing = False
recording = False
recording_thread = None
listen_duration = 2  # seconds avant qu'il s'arrête de record
quitpg = False
FACING_THRESHOLD = 0.07  # 15
AUDIO_THRESHOLD = 0.7  # 0 sourd 1 hypersensible

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


class SoundDetectionModule(ALModule):
    def __init__(self, name, IP, PORT):
        print("c'est parti 1")
        ALModule.__init__(self, name)
        self.memory = ALProxy("ALMemory", IP, PORT)
        self.memory.subscribeToEvent("SoundDetected", name, "onSoundDetected")
        self.sound_detection = ALProxy("ALSoundDetection", IP, PORT)
        self.sound_detection.setParameter("Sensibility", AUDIO_THRESHOLD)
        self.faceProxy = ALProxy("ALFaceDetection", IP, PORT)
        self.faceProxy.subscribe("Test_Face", 500, 0.0)

    def onSoundDetected(self, eventName, value, subscriberIdentifier):
        global recording, recording_thread
        print("Sound detected: ", value)
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
    global recording, recording_thread, facing
    #if facing:
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    tts.say("Hi!")
    audio_path = "/home/nao/audio/prompt.wav"
    audio_recorder = ALProxy("ALAudioRecorder", IP, PORT)
    audio_recorder.stopMicrophonesRecording()
    audio_recorder.startMicrophonesRecording(audio_path, "wav", 16000, [0, 0, 1, 0])
    # print("Recording started.")


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
    print("c'est parti 2")
    global SoundDetection, recording, myBroker, facing
    SoundDetection = SoundDetectionModule("SoundDetection", IP, PORT)
    basic_awareness = ALProxy("ALBasicAwareness", IP, PORT)
    motion = ALProxy("ALMotion", IP, PORT)


    for joint in used_joints:
        motion.setStiffnesses(joint, 1.0)
        # motion.setAngles(joint, 0, 0.5)

    for joint in ununsed_joints:
        motion.setStiffnesses(joint, 0.0)
        # motion.setAngles(joint, 0, 0.5)
    motion.wakeUp()
    basic_awareness.startAwareness()
    time.sleep(1.5)
    memValue = "FaceDetected"
    memoryProxy = ALProxy("ALMemory", IP, PORT)
    try:
        while not quitpg:
            time.sleep(0.1)
            if recording:
                print("Recording...")
            else:
                print("Waiting for sound...")
                '''print("Facing :", facing)
                val = memoryProxy.getData(memValue)
                if val and isinstance(val, list) and len(val) >= 2:
                    faceInfoArray = val[1]
                    for faceInfo in faceInfoArray:
                        if isinstance(faceInfo, list) and len(faceInfo) >= 2:
                            extraInfo = faceInfo[1]
                            leftEyePoints = round_points(extraInfo[3])
                            rightEyePoints = round_points(extraInfo[4])
                            if leftEyePoints != rightEyePoints:
                                diffdg1 = round(abs((leftEyePoints[0] - rightEyePoints[0])), 2)
                                diffdg2 = round(abs((rightEyePoints[0] - leftEyePoints[0])), 2)
                                print(diffdg1, diffdg2)
                                facing1 = diffdg1 > FACING_THRESHOLD
                                facing2 = diffdg2 > FACING_THRESHOLD
                                if facing1 or facing2:
                                    print("VISAGE DE FACE !!")
                                    facing = True
                                    # tts.say("oh!")
                                else:
                                    print("visage detecte mais pas de face")
                                    facing = False
                            else:
                                print("visage semi visible ")
                                facing = False

                else:
                    print("Aucun visage detecte")
                    facing = False'''
    except quitpg:
        print("Interrupted by user, shutting down")
        SoundDetection.memory.unsubscribeToEvent("SoundDetected", "SoundDetection")
        myBroker.shutdown()
        sys.exit(0)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main(IP, PORT)

    """