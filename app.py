import os
from flask import Flask, jsonify, render_template, request
import ollama

app = Flask(__name__)

PROMPT_PATH = os.getenv("PROMPT_PATH", "system_prompt.txt")
try:
  with open(PROMPT_PATH, "r") as f:
    BASE_SYSTEM_PROMPT = f.read()
except FileNotFoundError:
  BASE_SYSTEM_PROMPT = "You are Aerocloud AI, witty and intuitive."

MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3:8b-instruct-q4_K_M")

@app.route("/", methods=["GET"])
def home():
  return render_template("index.html", model_name=MODEL_NAME)

@app.route("/chat", methods=["POST"])
def chat():
  data = request.json or {}
  history = data.get("messages", [])
  user_name = data.get("userName", "User").strip() or "User"
  memories = data.get("memories", "").strip()

  if not history:
    return jsonify({"error": "No message provided"}), 400

  dynamic_prompt = (
      f"{BASE_SYSTEM_PROMPT}\n\n"
      f"Current user's name: {user_name}.\n"
  )
  if memories:
    dynamic_prompt += f"Saved facts/memories about the user:\n{memories}\n"

  conversation = [{"role": "system", "content": dynamic_prompt}] + history[-20:]

  try:
    response = ollama.chat(model=MODEL_NAME, messages=conversation)
    return jsonify({"response": response["message"]["content"]})
  except Exception as e:
    return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
