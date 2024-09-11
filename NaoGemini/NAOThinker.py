# -*- coding: UTF-8 -*-

# ===============================================
#  File       : NAOThinker.py
#  Author     : Milo Soulard (milosoulardgeii@gmail.com)
#  Python     : 3.x
#  Date       : Summer 2024
#  Description: Receives the audio prompt from the robot,
#               Speech to text it
#               Get a response from gemini
#               Save it to a txt file
# ===============================================
 
import speech_recognition as sr
import paramiko,sys,os
from dotenv import load_dotenv
import google.generativeai as genai
from llamaapi import LlamaAPI

nao_ip = "192.168.1.240"
username = password = "nao" # ssh credentials
remote_path = r"/home/nao/audio/prompt.wav" # path on the robot storage (keep it)
local_path = r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\prompt.wav" #change this with your own paths
txtpath = r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\prompt.txt"
historypath = r"D:\plymouth\code\NaoGeminiGestures\NaoGemini\promptHistory.txt"

"""client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12346))"""

def open_history():   
    with open(historypath, 'r') as file:
        my_string = file.read()#.decode('utf-8')
    return my_string

        
def prompt_download():  # get the audio from the robot and save it using ssh (paramiko)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(nao_ip, port=22, username=username, password=password)
        sftp = ssh.open_sftp()
        sftp.get(remote_path, local_path) #downloads the file
        print(f"File downloaded from {remote_path} to {local_path}")
    except Exception as e:
        print(f"Error while downloading : {str(e)}")
    finally:
        if sftp:
            sftp.close()
        ssh.close()


def recognition():  #use the audio and recognize it with google 
    r = sr.Recognizer()
    try:
        with sr.AudioFile(local_path) as source:
            audio = r.record(source)
        try:
            speech = r.recognize_google(audio)
            return speech #speech text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
    except FileNotFoundError:
        print(f"File not found: {local_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None


def ask_gemini(speech): # asks the AI for an answer
    load_dotenv() #load the key from the .env file
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.0-pro-latest")
    history = open_history()
    prompt = history + "\n here is your current chat history, use this to remember context from earlier : \n" + speech
    print(prompt) # response
    response = model.generate_content(prompt)
    responsetxt = response.text # accents would crash nao text to speech 
    responsetxt = responsetxt.replace(u'Î', u'I').replace(u'à', u'a').replace(u'â', u'a').replace(u'ä', u'a').replace(u'ç', u'c').replace(u'é', u'e').replace(u'è', u'e').replace(u'ê', u'e').replace(u'ë', u'e').replace(u'î', u'i').replace(u'ï', u'i').replace(u'ô', u'o').replace(u'ö', u'o').replace(u'ù', u'u').replace(u'û', u'u').replace(u'ü', u'u').replace(u'ÿ', u'y').replace(u'Æ', u'AE').replace(u'œ', u'oe')
    print("\n", responsetxt)
    return responsetxt

def ask_llama(speech): # asks the AI for an answer
    load_dotenv() #load the key from the .env file
    llama_key = os.getenv("LLAMA_API_KEY")
    llama = LlamaAPI(llama_key) # my llama api key
    history = open_history()
    prompt = history + "\n here is your current chat history, use this to remember context from earlier : \n" + speech
    print(prompt) # response 
    api_request_json = {
        "model": "llama-13b-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150,  # how detailed the response will be 
        "temperature": 0.8,  # how creative 
    }
    response = llama.run(api_request_json)
    responsetxt = response.json()["choices"][0]["message"]["content"]
    print("\n", responsetxt)
    return responsetxt

def save_to_txt(response): # saves the AI response to the text file read by NAOTalker 
    print("Saving to txt file {}".format(txtpath))
    try:
        with open(txtpath, "w") as file:
            file.write(response)
        print(f"Saved in {txtpath}\n")
    except Exception as e:
        print(f"Error : {str(e)}")


def save_prompt_and_response(prompt, response): # Saves the prompt and response in the history text file.
    try:
        entry = f"Prompt: {prompt}\nResponse: {response}\n{'-'*50}\n"
        with open(historypath, "a") as file:
            file.write(entry)
        print(f"Saved prompt and response in {historypath}\n")
    except Exception as e:
        print(f"Error: {str(e)}")


def main():
    prompt_download() #get the audio prompt from the robot 
    
    #client_socket.sendall("stop".encode())
    try:
        speech = recognition() # speech to text 
        if speech:
            print(f"Recognized speech: {speech}")
            print("\nprompt :", speech, "\n")

            """choose here between gemini and llama3"""

            #response = ask_gemini(speech)
            response = ask_llama(speech)

            save_to_txt(response) 
            save_prompt_and_response(speech, response) # saves the prompt and the response to txt files

            sys.exit(0)
        else:
            print("No speech recognized, or an error occurred.")
            response = "I didn't understand what you said. Can you repeat? "
            save_to_txt(response)
            sys.exit(0)
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down")


if __name__ == "__main__":
    main()
