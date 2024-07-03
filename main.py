import subprocess

python27path = r"[your python2.7 exe file path]"
python312path = r"[your python3 exe file path]"

def runListener():
    subprocess.run([python27path, r"[NAOListener.py path]"])

def runThinker():
    subprocess.run([python312path, r"[NAOThinker.py path]"])

def runTalker():
    subprocess.run([python27path, r"[NAOTalker.py path]"])

def main():
    runListener()   
    runThinker()
    runTalker()

if __name__ == "__main__":
    main()