import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response(prompt):
    chat = model.start_chat()
    res = chat.send_message(prompt)
    return res.text
