import subprocess

python27path = r"C:\Python27\python.exe"
python312path = r"C:\Users\soula\AppData\Local\Microsoft\WindowsApps\python3.exe"

def runListener():
    subprocess.run([python27path, r"D:\plymouth\code\NaoGemini\NAOListener.py"])

def runThinker():
    subprocess.run([python312path, r"D:\plymouth\code\NaoGemini\NAOThinker.py"])

def runTalker():
    subprocess.run([python27path, r"D:\plymouth\code\NaoGemini\NAOTalker.py"])

def main():
    while True:
        runListener()   
        runThinker()
        runTalker()

if __name__ == "__main__":
    main()