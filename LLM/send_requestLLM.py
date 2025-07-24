import urllib2
import json
import socket
import time
from naoqi import ALProxy

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        #Doesn't need to be reachable, just triggers the local IP logic
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception as e:
        ip = "127.0.0.1"
        print("Exception during get_ip: {}".format(e))
    finally:
        s.close()
    return ip


def send_request(prompt):
    req = urllib2.Request(URL, data=json.dumps({"model": MODEL_NAME, "prompt": prompt, "stream": False}), headers={"Content-Type": "application/json"})

    try:
        response = urllib2.urlopen(req)
        result = json.loads(response.read())
        reply = result.get("response", "No response found from LLM.")
        
    except Exception as e:
        reply = "Error contacting LLM."
        print("Exception: {}".format(e))

    TTS.say(str(reply))
    print(reply)
    
def SR_start():
    print("Listening for the word(s):", VOCABULARY)
    SR.subscribe("Ratchet")
    MEM.insertData("WordRecognized", []) #Clear the memory of the last recognized word.
    

LLM_IP = "169.254.49.133" #This needs to be the IP of the computer running LLM, but I am using my ethernet IP for testing during local-link.
LLM_PORT = "11434"
MODEL_NAME = "llama2"
NAO_IP = get_ip()  # Get the local IP address
NAO_PORT = 9559
TTS = ALProxy("ALTextToSpeech", NAO_IP, 9559)
#I should try to get the name of the NAO here somehow, so I can start listening for a prompt starting with "[NAO_NAME], ...".
URL = "http://{}:{}/api/generate".format(LLM_IP, LLM_PORT)
VOCABULARY = ["exit", "ratchet"]

if __name__ == "__main__":
    SR = ALProxy("ALSpeechRecognition", NAO_IP, 9559)
    MEM = ALProxy("ALMemory", NAO_IP, 9559)
    SR.setWordListAsVocabulary(VOCABULARY, False) #Set vocabulary for speech recognition. NAO will listen for the strings in VOCABULARY to be the first word spoken.
    SR_start()
    
    try:
        while True:
            word = MEM.getData("WordRecognized")
            if word and len(word) >= 2 and word[1] > .4:         
                if word[0] == "ratchet":   
                #NAO does not have open vocabulary speech recognition, so we will have to pipeline: record audio with ALAudioDeviceProxy (startMicrophonesRecording) -> PC -> Vosk(?) -> LLM -> ALTextToSpeech.
                #Because the LLM is slow (most likely model limitations and my slow laptop, though bigger responses will still be slow) we should try to this to work with streaming if possible.
                #Start recording audio to a file, so we can send it to the LLM.
                    print("Starting audio recording. Say your prompt after the 'listening'")
                    AUDIO = ALProxy("ALAudioDevice", NAO_IP, 9559)
                    TTS.say("Listening") #Maybe instead of this, just light the eyes green.
                    AUDIO.startMicrophonesRecording("/home/nao/recordings/audio/llm_prompt.wav")
                    #Wait for the user to finish speaking, then stop recording.
                    time.sleep(2) #Wait for 2 seconds to allow the user to start speaking. Might be better to just use a decimal value
                    #ISSUE: After the sleep, if the user doesn't make noise but is midsentence (like stopping to breathe), then the recording stops.
                    while MEM.getData("SpeechDetected") == True:
                        time.sleep(2) #Wait for a second before checking, should allow for ~ a second of silence.
                    AUDIO.stopMicrophonesRecording()
                    SR.unsubscribe("Ratchet")
                    print("Audio recording stopped. Sending request to LLM.")

                    # prompt = raw_input("Enter your prompt (or 'shutdown' to quit): ") #input() runs code in Python 2, not like Python 3.
                    # if prompt.lower() == "shutdown":
                    #     break
                    send_request("Hello")
                    SR_start()
                elif word[0] == "exit":
                    break
                
    except KeyboardInterrupt: #To make NAO stop listening when the program is interrupted.
        print("KeyboardInterrupt received, exiting.")
    finally:
        SR.unsubscribe("Ratchet")
        print("Unsubscribed from speech recognition.")
        TTS.say("Goodbye!")
        print("Exiting program.")