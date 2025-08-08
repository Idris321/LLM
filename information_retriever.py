# information_retriever.py
import json
import requests
import time

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# --- IMPORTANT ---
# Get the Gemini API key from the environment variable

# Global variable for the API URL and key
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
API_KEY = os.getenv("GEMINI_API_KEY")


def retrieve_information(query, documents):
    """
    Retrieves information from documents by sending a request to a generative API.
    The prompt is designed to elicit a specific and structured response.

    Args:
        query (str): The question to ask about the documents.
        documents (list): A list of strings, where each string is a document's content.

    Returns:
        list: A list of dictionaries with 'answer' and a mock 'score' from the API.
    """
    if not documents:
        return [{'answer': 'No documents available for search.', 'score': 0.0}]

    context = "\n\n".join(documents)

    # Use a more specific prompt to guide the API to the correct answer
    prompt = (
        f"You are a helpful assistant that analyzes insurance policy documents. "
        f"Based on the following policy documents, answer the user's query about a medical procedure. "
        f"Specifically, state if the procedure is covered, if it has a waiting period, or if it is excluded. "
        f"Do not invent information. Do not mention that you are using a model.\n\n"
        f"Policy Documents:\n{context}\n\n"
        f"User Query: {query}\n\n"
        f"Answer:"
    )

    retries = 3
    for i in range(retries):
        try:
            # Correctly construct the full URL with the API key
            full_url = f"{API_URL}?key={API_KEY}"
            
            chat_history = [{"role": "user", "parts": [{"text": prompt}]}]
            payload = {"contents": chat_history}
            
            headers = {"Content-Type": "application/json"}
            
            print(f"Sending request to API... (Attempt {i + 1}/{retries})")
            response = requests.post(
                full_url,
                headers=headers,
                data=json.dumps(payload)
            )
            response.raise_for_status()  # This will now correctly raise for 400 errors

            result = response.json()
            api_answer = result['candidates'][0]['content']['parts'][0]['text']

            # Assign a mock score based on the response content
            if "not found" in api_answer.lower() or "not covered" in api_answer.lower() or "excluded" in api_answer.lower():
                score = 0.1
            else:
                score = 0.95
            
            return [{'answer': api_answer, 'score': score}]

        except requests.exceptions.RequestException as e:
            print(f"API call failed: {e}")
            if i < retries - 1:
                wait_time = 2 ** (i + 1)
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                return [{'answer': f"Failed to connect to API after {retries} attempts: {e}", 'score': 0.0}]
        except (KeyError, IndexError) as e:
            print(f"API response format unexpected: {e}")
            return [{'answer': "API returned an unexpected response format.", 'score': 0.0}]

    return [{'answer': "An unexpected error occurred and the API call could not be completed.", 'score': 0.0}]


