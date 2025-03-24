# FastAPI and File Handling
from fastapi import FastAPI, File, UploadFile, HTTPException,Depends,Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import shutil
import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi import Request



# WebSocket and TTS
from backend.websocket import router as ws_router
from backend.tts import router as tts_router

# STT and LLM
from backend.stt import transcribe_audio
from backend.llm import generate_response

# Database and Document Processing
from backend.database import get_db_connection, create_session
from backend.extract_text import extract_text_from_pdf, split_text_into_chunks
from backend.embedder import store_embeddings_in_faiss, search_query_in_faiss
from sqlalchemy.orm import Session
from backend.database import create_new_session

templates = Jinja2Templates(directory="frontend/templates")


# Load environment variables
load_dotenv()

# Configuration
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

# Serve frontend files (HTML, CSS, JS)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Include WebSocket and TTS routes
app.include_router(ws_router)
app.include_router(tts_router)

# Redirect root to frontend
@app.get("/")
async def serve_frontend():
    return RedirectResponse(url="/frontend/index.html")

# Helper function to save uploaded files
def save_uploaded_file(file: UploadFile, upload_dir: str) -> str:
    file_path = os.path.join(upload_dir, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

# Helper function to store chunks in the database
def store_chunks_in_db(filename: str, chunks: list):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO document_chunks (filename, chunk_index, chunk_text) VALUES (%s, %s, %s)"
        values = [(filename, i, chunk) for i, chunk in enumerate(chunks)]

        cursor.executemany(query, values)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store chunks in database: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# File upload endpoint
@app.post('/upload/')
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = save_uploaded_file(file, UPLOAD_DIR)
        extracted_text = extract_text_from_pdf(file_path)
        text_chunks = split_text_into_chunks(extracted_text)
        store_chunks_in_db(file.filename, text_chunks)
        store_embeddings_in_faiss()
        return {
            "filename": file.filename,
            "message": "File uploaded, stored in database, and indexed in FAISS!"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Query endpoint
@app.post("/query/")
async def query_endpoint(user_query: str):
    try:
        results = search_query_in_faiss(user_query)
        llm_response = generate_response(user_query, results)
        return {"query": user_query, "results": results, "llm_response": llm_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during query: {str(e)}")

# LLM endpoint
@app.post("/generate/")
async def chat_with_ai(user_input: str):
    try:
        response = generate_response(user_input)
        return {"bot_response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

## Session Management

@app.post("/new-session")
async def new_session():
    session_id = create_new_session()  # Function that creates a new session in DB
    return {"session_id": session_id}


@app.get("/sessions")
def get_sessions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT session_id FROM chat_sessions")
    sessions = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return {"sessions": [s[0] for s in sessions]}


@app.get("/sidebar")
def get_sidebar(request: Request):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT session_id FROM chat_sessions")
    sessions = [s[0] for s in cursor.fetchall()]
    cursor.close()
    conn.close()

    return templates.TemplateResponse("sidebar.html", {"request": request, "sessions": sessions})



@app.get("/chat-history")
def get_chat_history(session_id: str = Query(...)):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT message, role FROM chat_messages WHERE session_id = %s ORDER BY timestamp ASC", (session_id,))
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"messages": messages}


@app.delete("/delete-session/{session_id}")
async def delete_session(session_id: str):
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        # Delete session from `chat_sessions`
        cursor.execute("DELETE FROM chat_sessions WHERE session_id = %s", (session_id,))
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Session not found")

        return {"message": "Session deleted successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        db.close()