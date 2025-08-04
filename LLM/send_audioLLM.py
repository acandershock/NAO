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

def send_audio_file_and_reply(AUDIO_FILE_PATH, FILE_NAME, TTS):
    print("Sending audio file to Vosk server for transcription.")
    #Prepare the multipart/form-data request to send the audio file.
    BOUNDARY = "WebKitFormBoundary7MA4YWxkTrZu0gW"
    data = []
    data.append("--" + BOUNDARY + "\r\n")
    data.append('Content-Disposition: form-data; name="NAO_audio"; filename="{}"\r\n'.format(FILE_NAME))
    data.append("Content-Type: audio/wav\r\n\r\n")
    with open(AUDIO_FILE_PATH, 'rb') as file:
        data.append(file.read())
    data.append("\r\n--" + BOUNDARY + "--\r\n")

    body = "".join(data) #Join the parts into a single string to send as the data of the request.
    
    #Send the audio file to Flask and get a reply from the LLM.
    req = urllib2.Request("http://169.254.44.35:5000/upload", data=body, headers={"Content-Type": "multipart/form-data; boundary={}".format(BOUNDARY), "Content-Length": str(len(body))})

    try:
        response = urllib2.urlopen(req)
        result = json.loads(response.read())
        reply = result.get("reply", "No reply found from LLM.")
        
    except Exception as e:
        reply = "Error contacting Flask host."
        print("Exception: {}".format(e))

    TTS.say(str(reply))
    print(reply)
    
def SR_start(SR, MEM, VOCABULARY):
    print("Listening for the word(s):", VOCABULARY)
    SR.subscribe("Ratchet")
    MEM.insertData("WordRecognized", []) #Clear the memory of the last recognized word.

if __name__ == "__main__":
    FILE_NAME = "LLM_prompt.wav"
    NAO_IP = get_ip()  # Get the local IP address
    NAO_PORT = 9559
    VOCABULARY = ["exit", "ratchet"]
    TTS = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
    SR = ALProxy("ALSpeechRecognition", NAO_IP, NAO_PORT)
    MEM = ALProxy("ALMemory", NAO_IP, NAO_PORT)
    SR.setWordListAsVocabulary(VOCABULARY, False) #Set vocabulary for speech recognition. NAO will listen for the strings in VOCABULARY to be the first word spoken.
    SR_start(SR, MEM, VOCABULARY)
    
    try:
        while True:
            word = MEM.getData("WordRecognized")
            # if word: print("Word: {} Confidence: {}".format(word[0], word[1]))
            # else: print("None.")
            if word and len(word) >= 2 and word[1] > .3:  
                if word[0] == "ratchet": #Start recording audio to a file, so we can send it to the LLM.
                    AUDIO_FILE_PATH = "/home/nao/recordings/audio/{}".format(FILE_NAME)
                    print("Starting audio recording. Say your prompt after the 'listening'")
                    AUDIO = ALProxy("ALAudioRecorder", NAO_IP, NAO_PORT)
                    TTS.say("Listening") #Maybe instead of this, just light the eyes green.
                    AUDIO.startMicrophonesRecording(AUDIO_FILE_PATH, "wav", 16000, [0, 0, 1, 0]) #Left, right, front, and rear microphones. Use 16kHz sample rate and mono (front) channel.
                    time.sleep(.75) #Give some time for the NAO to say "listening" and record. 1s is too long.
                    silence_duration = 0.0 #Used to have a smoother check for silence.

                    while True: #Keep recording until silence is detected for 2 seconds.
                        if MEM.getData("SpeechDetected"):
                            silence_duration = 0.0 #User resumed speaking.
                        else:
                            silence_duration += .2 #Increment silence duration by sleep time.
                            if silence_duration >= 2.0: #If silence is detected for 2 seconds, recording is stopped.
                                AUDIO.stopMicrophonesRecording()
                                SR.unsubscribe("Ratchet")
                                print("Audio recording stopped. Sending request to LLM.")
                                send_audio_file_and_reply(AUDIO_FILE_PATH, FILE_NAME, TTS)
                                break
                        time.sleep(.2) #Sleep to check for silence every n seconds.

                    SR_start(SR, MEM, VOCABULARY)
                elif word[0] == "exit":
                    break
                
    except KeyboardInterrupt: #To make NAO stop listening when the program is interrupted.
        print("KeyboardInterrupt received, exiting.")
    finally:
        SR.unsubscribe("Ratchet")
        print("Unsubscribed from speech recognition.")
        TTS.say("Goodbye!")
        print("Exiting program.")