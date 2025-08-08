from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import tempfile
import os
from utils.transcribe import transcribe_audio
from utils.generate_response import generate_response
from utils.text_to_speech import text_to_speech

app = Flask(__name__)
CORS(app)

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files and "text" not in request.form:
        return jsonify({"error": "No audio or text part in the request"}), 400

    user_input = ""
    if "audio" in request.files:
        audio = request.files["audio"]
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
            audio.save(temp_audio.name)
            user_input = transcribe_audio(temp_audio.name)
            os.remove(temp_audio.name)
    else:
        user_input = request.form["text"]

    if not user_input:
        return jsonify({"error": "Failed to get input"}), 400

    response_text = generate_response(user_input)
    audio_path = text_to_speech(response_text)

    return jsonify({
        "text": response_text,
        "audio_url": "/audio/" + os.path.basename(audio_path)
    })

@app.route("/audio/<filename>")
def get_audio(filename):
    filepath = os.path.join("static", "audio", filename)
    return send_file(filepath, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
