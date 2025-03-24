import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_response(user_input, faiss_results=None):
    """
    Generate a response using the Mistral 7B model via the Together API.
    """
    try:
        # Prepare headers and payload
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # Include user input and FAISS results in the request body
        context = "\n".join(faiss_results) if faiss_results else "No relevant result found."

        payload = {
            "model": "mistralai/Mistral-7B-Instruct-v0.2",
            "messages": [
                {"role": "system", "content": "Use the following relevant document snippets to answer the question:"},
                {"role": "system", "content": context},
                {"role": "user", "content": user_input}
            ]
        }

        # Make the API request
        logger.info(f"Sending request to Together API with payload: {payload}")
        response = requests.post(TOGETHER_API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse and return the response
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during API request: {e}")
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"Unexpected error: {str(e)}"