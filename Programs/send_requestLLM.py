import urllib2
import json
import socket
from naoqi import ALProxy

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable, just triggers the local IP logic
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def send_request(LLM_IP, LLM_PORT, MODEL_NAME, prompt, NAO_IP):
    url = "http://{}:{}/api/generate".format(LLM_IP, LLM_PORT)
    
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }
    
    headers = {"Content-Type": "application/json"}
    
    req = urllib2.Request(url, data=json.dumps(data), headers=headers)
    
    try:
        response = urllib2.urlopen(req)
        result = json.loads(response.read())
        reply = result.get("response", "No response found from LLM.")
        
    except Exception as e:
        reply = "Error contacting LLM."

    tts = ALProxy("ALTextToSpeech", NAO_IP, 9559)
    tts.say(reply)
    
if __name__ == "__main__":
    LLM_IP = "127.0.0.1" #10.129.9.107 #This needs to be the IP of the computer running LLM.
    LLM_PORT = "11434"
    MODEL_NAME = "tinyllama"
    prompt = "Hello."
    NAO_IP = get_ip()  # Get the local IP address
    send_request(LLM_IP, LLM_PORT, MODEL_NAME, prompt, NAO_IP)