# -*- coding: UTF-8 -*-

# ===============================================
#  File       : main.py
#  Author     : Milo Soulard
#  Python     : 3.x
#  Date       : Summer 2024
#  Description: Starts the program
# ===============================================

import subprocess
import threading

python27path = r"C:\Python27\python.exe"
python312path = r"C:\Users\soula\AppData\Local\Microsoft\WindowsApps\python3.exe"

def runCam():
    subprocess.run([python312path, r"D:\plymouth\code\NaoGeminiGestures\NaoGestures\NAOWatcher.py"])

def runNAO():
    subprocess.run([python27path, r"D:\plymouth\code\NaoGeminiGestures\NaoGestures\NAOMover.py"])
    

def main(): 
    thread1 = threading.Thread(target=runNAO)
    thread2 = threading.Thread(target=runCam)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()


