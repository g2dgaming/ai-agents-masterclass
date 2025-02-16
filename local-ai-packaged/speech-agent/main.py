import requests
import os
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

STT_URL = os.getenv("STT_URL")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
TTS_URL = os.getenv("TTS_URL")


@app.route("/process-audio", methods=["POST"])
def process_audio():
    if "file" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["file"]

    # Step 1: Convert speech to text (STT)
    response = requests.post(STT_URL, files={"audio": audio_file})
    if response.status_code != 200:
        return jsonify({"error": "STT failed", "details": response.text}), 500

    transcript = response.json().get("text", "")

    # Step 2: Send transcript to n8n workflow
    n8n_response = requests.post(N8N_WEBHOOK_URL, json={"text": transcript})
    if n8n_response.status_code != 200:
        return jsonify({"error": "n8n processing failed", "details": n8n_response.text}), 500

    processed_text = n8n_response.json().get("response", "")

    # Step 3: Convert processed text to speech (TTS)
    tts_response = requests.post(TTS_URL, json={"text": processed_text})
    if tts_response.status_code != 200:
        return jsonify({"error": "TTS failed", "details": tts_response.text}), 500

    # Save audio response to file
    with open("output.wav", "wb") as f:
        f.write(tts_response.content)

    return send_file("output.wav", mimetype="audio/wav")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
