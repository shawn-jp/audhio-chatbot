import base64
import requests
import os

def transcribe_audio(audio_path):
    with open(audio_path, "rb") as f:
        audio_data = f.read()

    base64_audio = base64.b64encode(audio_data).decode("utf-8")
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        "https://speech.googleapis.com/v1p1beta1/speech:recognize?key=" + os.getenv("GEMINI_API_KEY"),
        json={
            "config": {
                "encoding": "WEBM_OPUS",
                "languageCode": "ja-JP"
            },
            "audio": {
                "content": base64_audio
            }
        },
        headers=headers,
    )
    return response.json().get("results", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")
