from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from gtts import gTTS
from fastapi.responses import FileResponse
import os

router = APIRouter()

class TTSRequest(BaseModel):
    text: str

@router.post("/tts/")
async def text_to_speech(request: TTSRequest):
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty.")

        # Generate audio file from text
        tts = gTTS(text=request.text, lang="en")
        audio_path = "output.mp3"
        tts.save(audio_path)

        return FileResponse(audio_path, media_type="audio/mpeg", filename="output.mp3")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
