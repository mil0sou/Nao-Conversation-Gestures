import speech_recognition as sr
import paramiko
import os
from dotenv import load_dotenv
import google.generativeai as genai

nao_ip = "[your nao ip]"
username = password = "nao"
remote_path = r"/home/nao/audio/prompt.wav"
local_path = r"[prompt wav audio file location on your pc]"
txtpath = r"[prompt txt file location on your pc]"


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
    with sr.WavFile() as source:
        audio = r.record(source)
    try:
        speech = r.recognize_google(audio)
        return speech
    except LookupError:
        print("Could not understand audio")


def ask_gemini(speech):
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.0-pro-latest")
    response = model.generate_content(
        "You are a NAO robot, your name is NAO, and you exist at Plymouth university. Answer in 2 simple sentences."
        + speech
    )
    print("\n", response.text)
    return response.text


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
    speech = recognition()
    print("\nprompt :", speech, "\n")
    response = ask_gemini(speech)
    save_to_txt(response)


if __name__ == "__main__":
    main()
