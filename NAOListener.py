import time
from naoqi import ALProxy

nao_ip = "[your nao ip]"
nao_port = 9559
listen_duration = 7

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
