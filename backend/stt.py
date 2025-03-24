import whisper,warnings
import os


# Suppress the FP16 warning
warnings.filterwarnings("ignore", category=UserWarning)

# Load Whisper Model (Choose "base" for speed, "large" for accuracy)
model = whisper.load_model("base", device="cpu")  
def transcribe_audio(audio_file: str) -> str:
    """Convert speech to text using Whisper."""
    result = model.transcribe(audio_file, fp16=False)
    return result["text"]   
