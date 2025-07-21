import urllib2
import json
import socket
from naoqi import ALProxy

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        #Doesn't need to be reachable, just triggers the local IP logic
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

LLM_IP = "169.254.44.35" #This needs to be the IP of the computer running LLM, but I am using my ethernet IP for testing during local-link.
LLM_PORT = "11434"
MODEL_NAME = "llama2"
NAO_IP = get_ip()  # Get the local IP address
NAO_PORT = 9559
#I should try to get the name of the NAO here somehow, so I can start listening for a prompt starting with "[NAO_NAME], ...".
URL = "http://{}:{}/api/generate".format(LLM_IP, LLM_PORT)

def send_request(prompt):
    req = urllib2.Request(URL, data=json.dumps({"model": MODEL_NAME, "prompt": prompt, "stream": False}), headers={"Content-Type": "application/json"})

    try:
        response = urllib2.urlopen(req)
        result = json.loads(response.read())
        reply = result.get("response", "No response found from LLM.")
        
    except Exception as e:
        reply = "Error contacting LLM."
        print("Exception: {}".format(e))

    tts = ALProxy("ALTextToSpeech", NAO_IP, 9559)
    tts.say(str(reply))
    print(reply)
    
if __name__ == "__main__":
    while True:
        #NAO does not have open vocabulary speech recognition, so we will have to pipeline: record audio with ALAudioDeviceProxy (startMicrophonesRecording) -> PC -> Vosk(?) -> LLM -> ALTextToSpeech.
        #Because the LLM is slow (most likely model limitations and my slow laptop, though bigger responses will still be slow) we should try to this to work with streaming if possible.
        prompt = raw_input("Enter your prompt (or 'shutdown' to quit): ") #input() runs code in Python 2, not like Python 3.
        if prompt.lower() == "shutdown":
            break
        send_request(prompt)