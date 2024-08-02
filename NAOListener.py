# -*- coding: utf-8 -*-
import sys
from naoqi import ALProxy, ALModule, ALBroker
import time
import threading

nao_ip = "192.168.1.240"
nao_port = 9559
myBroker = ALBroker("myBroker", "0.0.0.0", 0, nao_ip, nao_port)
recording = False
recording_thread = None
listen_duration = 2 #seconds avant qu'il s'arrête de record
quitpg = False

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
    tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)
    tts.say("Hi!")

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
    main(nao_ip, nao_port)

    
################# ANCIEN CODE

"""import time
from naoqi import ALProxy

nao_ip = "192.168.1.240"
nao_port = 9559
listen_duration=3

def record_file():
    
    tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)
    tts.say("Hello. I am now recording. ")

    audio_path = "/home/nao/audio/prompt.wav"
    audio_recorder = ALProxy("ALAudioRecorder", nao_ip, nao_port)
    audio_recorder.stopMicrophonesRecording()
    audio_recorder.startMicrophonesRecording(audio_path, "wav", 16000, [0, 0, 1, 0])
    print("Recording...")
    time.sleep(listen_duration)
    
    audio_recorder.stopMicrophonesRecording()
    print("Recording stopped.")

record_file()
"""