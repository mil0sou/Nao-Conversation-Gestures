# NAO-Gemini/Llama Conversation Interface & Gesture imitation

The first project allows you to interact with Google's Gemini or Meta's LLama3 conversational AI through a NAO robot.
The second will make the robot move by imitating your body movements (with an azure kinect DK camera) (still in developement)

The robots eyes will turn yellow when he detects your face, then you can start speaking and the eyes will turn green when recording your request. 

## Installation

Follow these steps to set up the environment and install the necessary dependencies.

### Prerequisites

- Python 2.7 and Python 3.x
- `paramiko`
- `naoqi`
- `speech_recognition`
- `google.generativeai`
- `pykinect_azure`
- `socket`
- `numpy`

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/mil0sou/Nao-Conversation-Gestures
    cd NaoGeminiGestures/NaoGemini
    or 
    cd NaoGeminiGestures/NaoGestures
    ```


2. Install the dependencies:


    ```bash
    pip install numpy pykinect_azure llamaapi python-dotenv SpeechRecognition  
    pip install paramiko
    pip install -U google-generativeai
    ```
    
    download the 2.1.4 version of the SDK and the 32 bits python 2.7 msi file
    
    [direct naoqi download link](https://community-static.aldebaran.com/resources/2.1.4.13/sdk-python/pynaoqi-2.1.4.13.win32.exe)
    [python 2.7 32 bits windows installer](https://www.python.org/ftp/python/2.7.18/python-2.7.18.msi)
    [azure kinect body tracking sdk installer](https://www.microsoft.com/en-us/download/details.aspx?id=104221)
    [naoqi download page](https://www.aldebaran.com/en/support/nao-6/downloads-softwares)
    [naoqi installation guide](http://doc.aldebaran.com/2-1/dev/python/install_guide.html)
    [Microsoft Visual Package](https://www.microsoft.com/en-us/download/details.aspx?id=26999)        
   


4. Edit the code 

    Edit each file to use your NAO IP, your computer paths (IN MOST FILES !), your [google API key](https://ai.google.dev/gemini-api/docs/quickstart?hl=en&lang=python) or [llama API key](https://docs.llama-api.com/api-token)
    Create a file named .env and write your keys in it :
    ```bash
    GOOGLE_API_KEY= #your keys here
    LLAMA_API_KEY=
    ```

## Usage

Make sure NAO and your computer are connected to the same network. 

To start the conversation interface between the NAO robot and Google's Gemini AI, or gesture imitation : run in either folder:

```bash
python3 main.py
```

![code diagram](https://github.com/mil0sou/Nao-Conversation-Gestures/blob/main/NAO_Gemini_Diagram.png?raw=true)

