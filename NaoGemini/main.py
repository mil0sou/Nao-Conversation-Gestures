# -*- coding: utf-8 -*-
# ===============================================
#  File       : main.py
#  Author     : Milo Soulard
#  Python     : 3.x
#  Date       : Summer 2024
#  Description: Receives the response from gemini and makes the robot talk
# ===============================================

import subprocess
import threading

python27path = r"C:\Python27\python.exe"
python312path = r"C:\Users\soula\AppData\Local\Microsoft\WindowsApps\python3.exe"

def runListener():
    subprocess.run([python27path, r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\NAOFaceTracker.py"])

def runTracker():
    subprocess.run([python27path, r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\NAOFaceListener.py"])

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
    main()

