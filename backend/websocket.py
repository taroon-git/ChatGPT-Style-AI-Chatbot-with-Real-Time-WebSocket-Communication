from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import whisper
import tempfile
import numpy as np
import soundfile as sf
import asyncio
from backend.llm import generate_response
from backend.embedder import search_query_in_faiss
from backend.database import create_session, save_message


router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # 🔹 Step 1: Create a new session ID and send it to the client
    session_id = create_session()
    await websocket.send_text(f"SESSION_ID:{session_id}")  # Send session_id to client
    print(f"New chat session started: {session_id}")

    try:
        # 🔹 Step 2: Listen for messages and process them
        while True:
            try:
                user_message = await websocket.receive_text()  # Receive user input
                
                # Save user message
                save_message(session_id, user_message, "user")

                # Generate bot response
                faiss_results = search_query_in_faiss(user_message)
                bot_response = generate_response(user_message, faiss_results)

                # Save bot response
                save_message(session_id, bot_response, "bot")

                # Send bot response back to user
                await websocket.send_text(bot_response)

            except WebSocketDisconnect:
                print(f"User disconnected: session {session_id}")
                break  # Exit loop when user disconnects

            except Exception as e:
                print(f"Error: {e}")
                await websocket.send_text("Error processing your request.")
                continue  # Keep connection alive despite errors

    finally:
        await websocket.close()
        print(f"Chat session {session_id} closed")