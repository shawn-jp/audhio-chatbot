import os
import tempfile
import requests

def text_to_speech(text):
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "tts-1",
        "input": text,
        "voice": "shimmer"
    }
    response = requests.post(url, headers=headers, json=data)
    audio_path = os.path.join("static", "audio", next(tempfile._get_candidate_names()) + ".mp3")
    with open(audio_path, "wb") as f:
        f.write(response.content)
    return audio_path
