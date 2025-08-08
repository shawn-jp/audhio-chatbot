from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    text = data.get("text", "")
    reply = "こんにちは！" if text else "もう一度話してください。"
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
