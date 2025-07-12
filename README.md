#  AI Chatbot Assistant

A fully responsive, full-stack AI chatbot web app built with **Flask**, **Cohere API**, and **MongoDB**. The chatbot supports real-time conversation, stores chat history per session, and includes a clean, mobile-friendly UI.

---

## 📌 Features

-  AI-powered responses using [Cohere’s Language Models](https://cohere.com/)
-  Memory-aware conversations (uses last 10 messages as context)
-  Persistent chat history stored in MongoDB
-  Reset chat per session or delete all conversations
-  Clean, mobile-responsive UI with clear role-based message formatting
- 🛠 Built using Python (Flask), Vanilla JS, HTML, CSS, and MongoDB

---

## 🖥 Technologies Used

| Tech           | Purpose                             |
|----------------|-------------------------------------|
| **Flask**      | Backend framework (Python)          |
| **Cohere API** | Natural Language Understanding      |
| **MongoDB**    | NoSQL database to store chat history|
| **HTML/CSS**   | Frontend structure and styling      |
| **JavaScript** | Frontend logic and API interaction  |

---

##  Getting Started

###  Prerequisites

- Python 3.7+
- MongoDB installed and running locally (`mongodb://localhost:27017`)
- Cohere API key ([Get yours here](https://dashboard.cohere.com/api-keys))

###  Installation

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/chatbot-assistant.git
cd chatbot-assistant
Create Virtual Environment

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Set Your Cohere API Key
Open app.py and replace:

python
Copy code
co = cohere.Client("YOUR_API_KEY_HERE")
Start MongoDB
Ensure MongoDB is running on localhost:27017.

Run the Flask App

bash
Copy code
python app.py
Open your browser at http://127.0.0.1:5000

 API Endpoints
Method	Route	Description
GET	/	Load the chat interface
POST	/api	Send a message to the chatbot
POST	/reset	Clear current session chat history
GET	/history	Retrieve history for a session
DELETE	/history	Delete all chat history (admin use)

 UI & Responsive Design
Responsive layout optimized for mobile, tablet, and desktop views.

Flexbox and percentage-based widths ensure smooth resizing.

Auto-scrolling chat container.

Buttons and input fields are spaced for touch-friendliness.

Color-coded messages for clear distinction between User and Assistant.

 Project Structure
csharp
Copy code
chatbot-assistant/
│
├── app.py               # Main Flask app
├── templates/           # (Optional if using render_template_string)
├── static/              # For external CSS/JS (if extended)
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
 Future Improvements
Add login system to track users

Switch to a production server (e.g., Gunicorn + Nginx)

Support for exporting or emailing chat history

UI enhancements with animations and dark mode

Model switching between Cohere variants (command-r, etc.)
 Cohere Config (in app.py)
python
Copy code
response = co.chat(
    model="command",
    chat_history=history[-10:],  # Only last 10 for context
    message=user_msg,
    temperature=0.7,
    max_tokens=512
)
 License
This project is open-source and available under the MIT License.

