'''
server_llm.py

Ethan Miller
2025-07-31

This script sets up a Flask server that uses the Whisper model to transcribe audio files sent from a NAO robot.

* Needed ffmpeg for whisper to work properly on Windows
'''

from flask import Flask, request, jsonify
import whisper

app = Flask(__name__)

# CHANGE MODEL SRENGTH AS NEEDED
model = whisper.load_model("medium")

@app.route("/stt", methods=["POST"])
def stt():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file received"}), 400
    
    audio_file = request.files["audio"]
    temp_path = "nao_audio_whisper.wav"
    audio_file.save(temp_path)
    result = model.transcribe(temp_path)
    text = result["text"].strip()
    return jsonify({"transcript": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)