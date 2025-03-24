import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends
from backend.database import get_db_connection
from backend.vector_db import store_embeddings_in_faiss
from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt")

router = APIRouter()

UPLOAD_DIR = "uploaded_documents"

# ✅ Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    """
    Handles document upload and saves text chunks to the database.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # ✅ Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ✅ Extract text
    text_chunks = extract_text_from_pdf(file_path)

    # ✅ Store in database
    save_text_chunks_to_db(file.filename, text_chunks)

    # ✅ Generate & store embeddings in FAISS
    store_embeddings_in_faiss()

    return {"message": "File uploaded and processed successfully!", "filename": file.filename}


def extract_text_from_pdf(pdf_path): 
    """
    Extracts and tokenizes text from a PDF file into small chunks.
    """
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + " "

    text = text.strip()

    # ✅ Split into sentences using NLTK
    sentences = sent_tokenize(text)

    # ✅ Chunking logic (combine sentences into chunks of ~3 sentences)
    chunks = []
    chunk_size = 3
    for i in range(0, len(sentences), chunk_size):
        chunk = " ".join(sentences[i : i + chunk_size])
        chunks.append(chunk)

    return chunks


def save_text_chunks_to_db(filename, text_chunks):
    """
    Stores extracted text chunks in MySQL.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    for index, chunk in enumerate(text_chunks):
        cursor.execute(
            "INSERT INTO document_chunks (filename, chunk_index, chunk_text) VALUES (%s, %s, %s)",
            (filename, index, chunk),
        )

    conn.commit()
    cursor.close()
    conn.close()
