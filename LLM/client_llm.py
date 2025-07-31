'''
client_llm.py

Ethan Miller
2025-07-31

This script records audio from a NAO robot, sends it to a whisper speech-to-text server,
and then sends the transcribed text to a llama2 LLM to get a response.
'''

from naoqi import ALProxy
import requests, time, os

# Setup
NAO_IP = "127.0.0.1"
NAO_PORT = 9559
RAW_WAV = "/home/nao/recordings/audio/nao_audio.wav"

# CHANGE LOCAL_LINK IP FOR SERVER PC !!!
STT_SERVER_URL = "http://169.254.25.129:5000/stt"
LLM_SERVER_URL = "http://169.254.25.129:11434/api/generate"

tts = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
audio = ALProxy("ALAudioDevice", NAO_IP, NAO_PORT)

# Record audio for LLM
def record_audio(duration):
    if os.path.exists(RAW_WAV):
        os.remove(RAW_WAV)

    print("Recording for {} seconds...".format(duration))
    tts.say("Recording for {} seconds...".format(duration))
    audio.startMicrophonesRecording(RAW_WAV)
    time.sleep(duration)
    audio.stopMicrophonesRecording()
    print("Recording complete!")
    tts.say("Recording complete!")
    return RAW_WAV

# POST to whisper speech-to-text server
def speech_to_text(filename):
    with open(filename, 'rb') as f:
        files = {'audio': f}
        r = requests.post(STT_SERVER_URL, files=files)
    try:
        data = r.json()
        transcript = data.get("transcript", "")
        return str(transcript)
    except:
        print("STT server error:", r.status_code, r.text)
        return ""

# Prompt llama2 LLM
def prompt_llm(prompt):
    payload = {"model": "llama2", "prompt": prompt, "stream": False}
    r = requests.post(LLM_SERVER_URL, json=payload)
    try:
        data = r.json()
        response = data.get("response") or "LLM returned no response."
        return str(response)
    except:
        print("LLM server error:", r.status_code, r.text)
        return "Error contacting LLM."

if __name__ == "__main__":
    print("Let's get started! Please speak clearly. Say exit to quit.")
    tts.say("Let's get started! Please speak clearly. Say exit to quit.")

    while True:
        # CHANGE DURATION AS NEEDED
        filename = record_audio(5)
        print("Processing your speech.")
        tts.say("Processing your speech.")

        transcript = speech_to_text(filename)
        if transcript.lower() == "exit" or transcript.lower() == "exit.":
            print("Bye Bye now and take care!")
            tts.say("Bye Bye now and take care!")
            break
        elif not transcript:
            print("I could not understand any speech.")
            break
        else:
            print("You said:" + transcript)
            tts.say("You said " + transcript)

            print("Prompting LLM")
            tts.say("Prompting LLM")
            response = prompt_llm(transcript)
            print(response)
            tts.say(response)
