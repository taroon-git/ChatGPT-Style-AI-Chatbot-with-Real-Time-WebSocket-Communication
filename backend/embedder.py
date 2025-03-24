import faiss
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from backend.database import get_db_connection

# Load SBERT model
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

FAISS_INDEX_PATH = "faiss_index/faiss_index"

def get_text_chunks_from_db():
    """
    Retrieve all text chunks from MySQL.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, chunk_text FROM document_chunks")
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return results  # Returns [(id, chunk_text), (id, chunk_text), ...]

def generate_embeddings(text_list):
    """
    Generate SBERT embeddings for a list of text chunks.
    """
    return sbert_model.encode(text_list, convert_to_numpy=True)

def store_embeddings_in_faiss():
    """
    Retrieve text chunks from MySQL, generate embeddings, and store in FAISS.
    """
    text_data = get_text_chunks_from_db()
    
    if not text_data:
        print("No text chunks found in database.")
        return

    ids, texts = zip(*text_data)
    
    # Generate embeddings
    embeddings = generate_embeddings(list(texts))
    
    # Create FAISS index
    dimension = embeddings.shape[1]  # Embedding size
    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(embeddings)  # Add embeddings to FAISS
    
    # ✅ Ensure the FAISS directory exists before saving the index
    os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)

    # Save FAISS index
    faiss.write_index(faiss_index, FAISS_INDEX_PATH)
    print(f"FAISS index stored at: {FAISS_INDEX_PATH}")



def search_query_in_faiss(query, top_k=3):
    """
    Searches the FAISS index for the most relevant text chunks based on the query.
    
    :param query: The user input query (text).
    :param top_k: Number of closest matches to retrieve.
    :return: List of matching text chunks.
    """
    # Load FAISS index
    faiss_index = faiss.read_index(FAISS_INDEX_PATH)

    # Convert query to embedding
    query_embedding = sbert_model.encode([query])
    query_embedding = np.array(query_embedding).astype('float32')

    # Perform similarity search in FAISS
    distances, indices = faiss_index.search(query_embedding, top_k)

    # Retrieve matching text chunks from MySQL
    conn = get_db_connection()
    cursor = conn.cursor()

    matching_chunks = []
    for idx in indices[0]:  # Get the indices of top matches
        if idx == -1:  # If no valid match, continue
            continue
        
        cursor.execute("SELECT chunk_text FROM document_chunks WHERE id = %s", (int(idx),))
        result = cursor.fetchone()
        if result:
            matching_chunks.append(result[0])

    conn.close()
    
    return matching_chunks