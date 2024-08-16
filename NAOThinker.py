import speech_recognition as sr
import paramiko,sys,os
from dotenv import load_dotenv
import google.generativeai as genai
from llamaapi import LlamaAPI

nao_ip = "192.168.1.240"
username = password = "nao"
remote_path = r"/home/nao/audio/prompt.wav"
local_path = r"D:\plymouth\audioprompt\prompt.wav"
txtpath = r"D:\plymouth\audioprompt\prompt.txt"
default_prompt = """You are a NAO robot, your name is NAO, 
and you exist at Plymouth university, 
but don't talk about it unless you're asked. 
You know everything about everything. 
Answer to the following question in two simple sentences : """

def prompt_download():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(nao_ip, port=22, username=username, password=password)
        sftp = ssh.open_sftp()
        sftp.get(remote_path, local_path)
        print(f"File downloaded from {remote_path} to {local_path}")
    except Exception as e:
        print(f"Error while downloading : {str(e)}")
    finally:
        if sftp:
            sftp.close()
        ssh.close()


def recognition():
    r = sr.Recognizer()
    audio_file_path = r"D:\plymouth\audioprompt\prompt.wav"

    try:
        with sr.AudioFile(audio_file_path) as source:
            audio = r.record(source)
        try:
            speech = r.recognize_google(audio)
            return speech
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
    except FileNotFoundError:
        print(f"File not found: {audio_file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None


def ask_gemini(speech):
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.0-pro-latest")
    response = model.generate_content(default_prompt + speech)
    responsetxt = response.text
    responsetxt = responsetxt.replace(u'à', u'a').replace(u'é', u'e').replace(u'è', u'e').replace(u'ê', u'e').replace(u'ù', u'u').replace(u'ç', u'c').replace(u'ô', u'o')
    print("\n", responsetxt)
    return responsetxt

def ask_llama(speech):
    llama = LlamaAPI("LL-pZPlvP5fCPF8feUFty3uooyp02FiiJB8wluy7wpWT3ivgwi7ImHLtTyGZAMF10Wi")

    prompt = default_prompt + speech
    api_request_json = {
        "model": "llama-13b-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150,  
        "temperature": 0.8,  
    }
    response = llama.run(api_request_json)
    responsetxt = response.json()["choices"][0]["message"]["content"]
    print("\n", responsetxt)
    return responsetxt

def save_to_txt(response):
    print("Saving to txt file {}".format(txtpath))
    try:
        with open(txtpath, "w") as file:
            file.write(response)
        print(f"Saved in {txtpath}\n")
    except Exception as e:
        print(f"Error : {str(e)}")


def main():
    prompt_download()
    try:
        speech = recognition()
        if speech:
            print(f"Recognized speech: {speech}")
            print("\nprompt :", speech, "\n")
            #response = ask_gemini(speech)
            response = ask_llama(speech)
            save_to_txt(response)
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
