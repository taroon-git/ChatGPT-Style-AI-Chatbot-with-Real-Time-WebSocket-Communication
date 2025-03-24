import PyPDF2
import re

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.
    """
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    
    return text

def split_text_into_chunks(text: str, chunk_size: int = 500) -> list:
    """
    Splits the extracted text into smaller chunks of `chunk_size` characters.
    """
    text = re.sub(r"\s+", " ", text).strip()  
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
