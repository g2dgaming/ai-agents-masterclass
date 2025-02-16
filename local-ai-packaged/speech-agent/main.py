import os
import requests
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Service URLs
N8N_AGENT_URL = os.getenv("N8N_AGENT_URL", "http://n8n:5678/webhook/speech-processing")
TTS_URL = os.getenv("TTS_URL", "http://melotts-tts:8080/tts")

@app.route("/process-text", methods=["POST"])
def process_text():
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request"}), 400

    text = data["text"]

    # Step 1: Send text to n8n agent
    try:
        n8n_response = requests.post(N8N_AGENT_URL, json={"text": text})
        if n8n_response.status_code != 200:
            return jsonify({"error": "Failed to process text with n8n", "details": n8n_response.text}), 500
    except Exception as e:
        return jsonify({"error": f"n8n API request failed: {str(e)}"}), 500

    response_data = n8n_response.json()
    processed_text = response_data.get("processed_text")

    if not processed_text:
        return jsonify({"error": "No processed text returned by n8n"}), 500

    # Step 2: Convert processed text to speech using TTS
    try:
        tts_response = requests.post(TTS_URL, json={"text": processed_text})
        if tts_response.status_code != 200:
            return jsonify({"error": "TTS conversion failed", "details": tts_response.text}), 500

        # Save speech output
        speech_file = "output.wav"
        with open(speech_file, "wb") as f:
            f.write(tts_response.content)

        return send_file(speech_file, mimetype="audio/wav")
    except Exception as e:
        return jsonify({"error": f"TTS conversion failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
