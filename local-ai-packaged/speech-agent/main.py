import os
import requests
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Service URLs
STT_URL = os.getenv("STT_URL", "http://deepspeech-stt:8080/stt")  # Speech-to-Text
N8N_AGENT_URL = os.getenv("N8N_AGENT_URL", "http://n8n:5678/webhook/speech-processing")  # n8n workflow
TTS_URL = os.getenv("TTS_URL", "http://melotts-tts:8080/tts")  # Text-to-Speech

@app.route("/process-audio", methods=["POST"])
def process_audio():
    """Receives an audio file, applies STT, sends to n8n, and converts response to speech."""
    if "audio" not in request.files:
        return jsonify({"error": "Missing 'audio' file in request"}), 400

    audio_file = request.files["audio"]
    audio_path = "input.wav"
    audio_file.save(audio_path)

    # Step 1: Convert speech to text using STT
    try:
        with open(audio_path, "rb") as f:
            stt_response = requests.post(STT_URL, files={"audio": f})

        if stt_response.status_code != 200:
            return jsonify({"error": "STT conversion failed", "details": stt_response.text}), 500

        recognized_text = stt_response.json().get("text")
        if not recognized_text:
            return jsonify({"error": "No text recognized from audio"}), 500
    except Exception as e:
        return jsonify({"error": f"STT conversion failed: {str(e)}"}), 500

    # Step 2: Send recognized text to n8n agent for processing
    try:
        n8n_response = requests.post(N8N_AGENT_URL, json={"text": recognized_text})
        if n8n_response.status_code != 200:
            return jsonify({"error": "Failed to process text with n8n", "details": n8n_response.text}), 500

        processed_text = n8n_response.json().get("processed_text")
        if not processed_text:
            return jsonify({"error": "No processed text returned by n8n"}), 500
    except Exception as e:
        return jsonify({"error": f"n8n API request failed: {str(e)}"}), 500

    # Step 3: Convert processed text to speech using TTS
    try:
        tts_response = requests.post(TTS_URL, json={"text": processed_text})
        if tts_response.status_code != 200:
            return jsonify({"error": "TTS conversion failed", "details": tts_response.text}), 500

        # Save and return the generated speech file
        speech_file = "output.wav"
        with open(speech_file, "wb") as f:
            f.write(tts_response.content)

        return send_file(speech_file, mimetype="audio/wav")
    except Exception as e:
        return jsonify({"error": f"TTS conversion failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
