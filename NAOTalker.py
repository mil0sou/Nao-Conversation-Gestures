from naoqi import ALProxy

nao_ip = "[your nao ip]"
nao_port = 9559
txtpath = r"[prompt txt file location on your pc]"

def open_response():
    with open(txtpath, 'r') as file:
        my_string = file.read().decode('utf-8')
    print "Response :"
    print my_string
    return my_string


def say_response(response):
    tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)
    response = str(response).encode('utf-8')
    tts.say(response)

response = open_response()
say_response(response)
