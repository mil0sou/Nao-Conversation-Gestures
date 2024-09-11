# -*- coding: utf-8 -*-
# ===============================================
#  File       : main.py
#  Author     : Milo Soulard (milosoulardgeii@gmail.com)
#  Python     : 3.x
#  Date       : Summer 2024
#  Description: Receives the response from gemini and makes the robot talk
# ===============================================

import subprocess
import threading
import os
import paramiko


historypath = r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\promptHistory.txt"
python27path = r"C:\Python27\python.exe"
python312path = r"C:\Users\soula\AppData\Local\Microsoft\WindowsApps\python3.exe"
hostname = "192.168.1.240"
username = password = "nao"

default_prompt = """You are a NAO robot, your name is NAO, 
and you exist at Plymouth university, 
but don't talk about it unless you're asked. 
You know everything about everything. 
Answer to the following question in two simple sentences: 
--------------------------------------------------
"""

def reset_txt_file():
    try:
        if os.path.exists(historypath):
            os.remove(historypath)
            print(f"{historypath} has been reset.")
        with open(historypath, "w") as file:
            file.write(default_prompt + "\n")
        print(f"Default prompt has been written to {historypath}\n")
    except Exception as e:
        print(f"Error: {str(e)}")



def runTracker():
    subprocess.run([python27path, r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\NAOFaceTracker.py"])

def runListener():
    subprocess.run([python27path, r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\NAOFaceListener.py"])

def runThinker():
    subprocess.run([python312path, r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\NAOThinker.py"])

def runTalker():
    subprocess.run([python27path, r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\NAOTalker.py"])

def main():
    reset_txt_file()
    while True:
        listener1_thread = threading.Thread(target=runTracker)
        listener2_thread = threading.Thread(target=runListener)
        
        listener1_thread.start()
        listener2_thread.start()
        
        while listener1_thread.is_alive() and listener2_thread.is_alive():
            listener1_thread.join(timeout=1)
            listener2_thread.join(timeout=1)
 
        # when one of Tracker or Listener ends, start those 2
        runThinker()
        runTalker()

if __name__ == "__main__":
    main()

