# 🌟 ChatGPT-Style AI Chatbot with Real-Time WebSocket Communication

## 🌐 Project Description
This project is an **AI-powered chatbot** that provides **real-time chat capabilities** with session-based history management. Built using **FastAPI**, the chatbot integrates **Mistral 7B (int4 quantized)** for response generation and **sBERT** for efficient text embedding and similarity matching.

The **frontend** is a **ChatGPT-style UI**, allowing users to chat via text and voice (TTS/STT). It supports **session management**, **chat history storage**, and **chat sharing via links**.

---

## 🚀 Key Features

✅ **Real-Time Communication** – Uses **WebSockets** for instant message exchange.  
✅ **AI-Powered Responses** – Uses **Mistral 7B** for chatbot responses.  
✅ **Session-Based History** – Users can resume previous conversations seamlessly.  
✅ **Speech-to-Text (STT) & Text-to-Speech (TTS)** – Voice input & AI-generated audio responses.  
✅ **Chat History Management** – Store, retrieve, and manage chat sessions effectively.  
✅ **Clear Chats & New Sessions** – Users can start fresh conversations anytime.  
✅ **Chat Link Sharing** – Generate & share chat links for easy access.  
✅ **User-Friendly UI** – Frontend UI closely resembles **ChatGPT's interface**.  

---

## 🛠 Tech Stack

### 🔹 Backend:
- **FastAPI** – For building the REST API & WebSocket communication.
- **Mistral 7B (int4 quantized)** – For AI-generated responses.
- **sBERT (Sentence-BERT)** – For text similarity search & embeddings.
- **WebSockets** – Enables real-time chat functionality.
- **MySQL** – Stores chat history, sessions, and message data.

### 🔹 Frontend:
- **HTML, CSS, JavaScript** – ChatGPT-style UI for a smooth user experience.
- **WebSocket Integration** – Ensures live chat updates.

---

## 📺 Project Structure
```
STT-TTS-Chatbot/
│-- backend/
│   │-- main.py              # FastAPI app entry point
│   │-- websocket.py         # WebSocket handling
│   │-- database.py          # MySQL database interactions
│   │-- document_process.py  # Document processing (if applicable)
│   │-- embedder.py          # Text embedding for chatbot search
│   │-- extract_text.py      # Text extraction from documents
│   │-- llm.py               # AI model integration (Mistral 7B)
│   │-- stt.py               # Speech-to-Text (Whisper-based)
│   │-- tts.py               # Text-to-Speech
│-- frontend/
│   │-- index.html           # Main Chat UI
│   │-- script.js            # Handles chat WebSocket & UI updates
│   │-- styles.css           # Custom styling for the UI
│-- uploads/                 # Stores uploaded files
│-- venv/                    # Python Virtual Environment
│-- .env                     # Environment variables
│-- README.md                # Project Documentation
```

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/chatgpt-style-chatbot.git
cd chatgpt-style-chatbot
```

### 2️⃣ Create a Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Set Up the .env File
Create a `.env` file in the root directory and configure it with your database & model details.  
Example:
```env
DATABASE_URL=mysql://username:password@localhost/chatbot_db
MODEL_PATH=mistralai/Mistral-7B-Instruct-v0.2
```

### 4️⃣ Run the FastAPI Backend
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5️⃣ Open the Chat UI
- Open `frontend/index.html` in a browser.
- Start chatting with real-time AI responses! 🎧💬

---

## 📀 API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/chat/sessions` | Retrieve all chat sessions |
| `POST` | `/chat/start` | Start a new chat session |
| `POST` | `/chat/message` | Send a message & get AI response |
| `DELETE` | `/chat/clear` | Clear chat history |
| `GET` | `/chat/share/{session_id}` | Get sharable chat link |

---

## 🎯 Future Enhancements

🚀 **WhatsApp Integration** – Extend chat capabilities to WhatsApp.  
🚀 **User Authentication** – Secure sessions with login functionality.  
🚀 **Enhanced Caching** – Use Redis to optimize message retrieval.  

---

## ⭐ Contributing
Pull requests are welcome! For major changes, please open an issue first.

---

## 📚 License
This project is **open-source** under the (-_-) License.

