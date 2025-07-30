from flask import Flask, request, jsonify
from vosk import Model, KaldiRecognizer
import wave
import json
import requests

app = Flask(__name__) #Initialize Flask app.
model = Model("vosk") #Load Vosk model.

@app.route('/upload', methods=['POST']) #Tell Flask what URL triggers upload function.
def upload():
    audio = request.files['NAO_audio'] #Get NAO_audio file from HTTP request.
    if not audio.filename.endswith(".wav"): #Ensure the file is a .wav file.
        return jsonify({"error": "Invalid file format. Only .wav accepted."}), 400 #400 is bad request HTTP status code.
    #Save audio file in a temp directory.
    filepath = "/tmp/NAO_audio.wav"
    audio.save(filepath)
    
    with wave.open(filepath, "rb") as wf:
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        rec.AcceptWaveform(wf.readframes(wf.getnframes()))
        transcript = (json.loads(rec.FinalResult())).get("text", "")
        print("Transcript:", transcript)

    try: #Send transcript to LLM to get a reply. Using localhost since same machine running Vosk and Flask should be hosting LLM.
        llm_response = requests.post("http://localhost:11434/api/generate", json={"model": "llama2", "prompt": transcript, "stream": False})
        reply = llm_response.json().get("response", "No response found from LLM.")
    except Exception as e:
        reply = "Error getting a reply."
        print("LLM error:", e)

    return jsonify({"reply": reply}), 200 #200 is OK HTTP status code.

app.run(host="169.254.49.133", port=5000) #Change host to IP of the network PC and NAO are connected to.
