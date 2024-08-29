# NAO-Gemini Conversation Interface & Gesture imitation

The first project allows you to interact with Google's Gemini or Meta's LLama3 conversational AI through a NAO robot.
The second 

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
    pip install paramiko speech_recognition google.generativeai
    ```

    [naoqi installation guide](http://doc.aldebaran.com/2-8/dev/python/install_guide.html) 

3. Edit the code 

    Edit each file to use your NAO IP, your computer paths, your [google API key](https://ai.google.dev/gemini-api/docs/quickstart?hl=en&lang=python)

## Usage

Make sure NAO and your computer are connected to the same network. 
To start the conversation interface between the NAO robot and Google's Gemini AI, or gesture imitation : run in either folder:

```bash
python3 main.py
```
