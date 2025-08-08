from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__, static_url_path="", static_folder=".")
CORS(app)

@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

@app.route("/api/audio", methods=["POST"])
def audio_input():
    return jsonify({"reply": "（音声入力の認識部分は未実装です）"})

@app.route("/api/text", methods=["POST"])
def text_input():
    data = request.get_json()
    user_text = data.get("text", "")
    prompt = f"""あなたは音声対話型の日本語アシスタントです。
以下のユーザーの発言に対し、自然な会話として違和感のない返答を日本語で1～2文で簡潔に返してください。
文語調ではなく、口語・話し言葉でお願いします。

ユーザーの発言:「{user_text}」
"""
    response = model.generate_content(prompt)
    return jsonify({"reply": response.text.strip()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)