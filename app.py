from flask import Flask, request, jsonify, render_template_string
from pymongo import MongoClient
import cohere

app = Flask(__name__)

co = cohere.Client("wR8puerz304zm85slzUcWt6g7tpeh1zNqQIAznhw")
client = MongoClient("mongodb://localhost:27017")
db = client["chatbot_db"]
history_collection = db["chat_history"]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AI Chatbot Assistant</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      background: linear-gradient(to right, #e0eafc, #cfdef3);
      margin: 0;
      padding: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    header {
      background-color: #4a90e2;
      color: white;
      width: 100%;
      padding: 1rem;
      text-align: center;
      font-size: 1.75rem;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    #chat-box {
      background: white;
      width: 95%;
      max-width: 700px;
      height: 60vh;
      margin-top: 20px;
      border-radius: 12px;
      padding: 1rem;
      overflow-y: auto;
      box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    .message {
      margin-bottom: 1rem;
      padding: 10px 14px;
      border-radius: 16px;
      max-width: 85%;
      animation: fadeIn 0.4s ease-in;
    }
    .user {
      background-color: #d9fdd3;
      align-self: flex-end;
      text-align: right;
      margin-left: auto;
    }
    .bot {
      background-color: #f1f0f0;
      align-self: flex-start;
      text-align: left;
      margin-right: auto;
    }
    .input-section {
      width: 95%;
      max-width: 700px;
      display: flex;
      gap: 0.5rem;
      margin: 20px 0;
    }
    #user-input {
      flex-grow: 1;
      border-radius: 10px;
      padding: 0.75rem;
      border: 1px solid #ccc;
    }
    button {
      border-radius: 10px;
      padding: 0.75rem 1.25rem;
      border: none;
      font-weight: 500;
      transition: all 0.2s ease;
    }
    button:hover {
      transform: scale(1.03);
    }
    .btn-send {
      background-color: #4a90e2;
      color: white;
    }
    .btn-reset {
      background-color: #f0f0f0;
      color: #333;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body>
  <header>AI Chatbot Assistant</header>
  <div id="chat-box" class="d-flex flex-column"></div>
  <div class="input-section">
    <input type="text" id="user-input" class="form-control" placeholder="Type a message...">
    <button class="btn btn-send" onclick="sendMessage()">Send</button>
    <button class="btn btn-reset" onclick="resetChat()">Reset</button>
  </div>

  <script>
    const sessionId = "guest_session";

    function appendMessage(sender, text) {
      const chatBox = document.getElementById("chat-box");
      const div = document.createElement("div");
      div.className = "message " + (sender === "Bot" ? "bot" : "user");
      div.innerHTML = `<strong>${sender}:</strong><br>${text}`;
      chatBox.appendChild(div);
      chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function sendMessage() {
      const input = document.getElementById("user-input");
      const message = input.value.trim();
      if (!message) return;
      appendMessage("You", message);
      input.value = "";

      try {
        const res = await fetch("/api", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message, session_id: sessionId })
        });
        const data = await res.json();
        appendMessage("Bot", data.reply);
      } catch {
        appendMessage("Bot", "Oops! Something went wrong. Please try again later.");
      }
    }

    async function resetChat() {
      await fetch("/reset", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId })
      });
      document.getElementById("chat-box").innerHTML = "";
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "").strip()
    session_id = data.get("session_id", "default_session")
    if not user_msg:
        return jsonify({"reply": "Your message appears to be empty. Please type something."}), 400

    def map_role(role):
        if role.lower() == "user":
            return "User"
        if role.lower() in ("assistant", "chatbot"):
            return "Chatbot"
        return role

    try:
        history_cursor = history_collection.find({"session_id": session_id}).sort("_id", 1)
        history = [{"role": map_role(h["role"]), "message": h["message"]} for h in history_cursor]

        response = co.chat(
            model="command",
            chat_history=history[-10:],
            message=user_msg,
            temperature=0.7,
            max_tokens=512
        )
        bot_reply = response.text.strip()

        history_collection.insert_many([
            {"session_id": session_id, "role": "User", "message": user_msg},
            {"session_id": session_id, "role": "Chatbot", "message": bot_reply}
        ])
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"Oops! Something went wrong. ({e})"}), 500

@app.route("/reset", methods=["POST"])
def reset_chat():
    session_id = request.json.get("session_id", "default_session")
    history_collection.delete_many({"session_id": session_id})
    return "", 204

@app.route("/history", methods=["GET"])
def get_history():
    session_id = request.args.get("session_id", "default_session")
    history_cursor = history_collection.find({"session_id": session_id}).sort("_id", 1)
    history = [{"role": h["role"], "message": h["message"]} for h in history_cursor]
    return jsonify({"history": history})

@app.route("/history", methods=["DELETE"])
def delete_history():
    history_collection.delete_many({})
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
