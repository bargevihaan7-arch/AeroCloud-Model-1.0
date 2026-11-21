import urllib.request
import json

MODEL = "llama3:8b-instruct-q4_K_M"
OLLAMA_URL = "http://localhost:11434/api/chat"

print(f"--- Aerocloud Core Playground ({MODEL}) ---")
system_prompt = input("Enter system brain/instructions (or press Enter for default): ").strip()
if not system_prompt:
    system_prompt = "You are a helpful, direct assistant."

messages = [{"role": "system", "content": system_prompt}]

while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        break
    
    messages.append({"role": "user", "content": user_input})
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }
    
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            reply = result["message"]["content"]
            print(f"\nAI: {reply}")
            messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        print(f"Error connecting to Ollama container: {e}")
