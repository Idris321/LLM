# app.py
import os
import json
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

# Make sure all your local Python files are in the same directory as app.py
from query_parser import parse_query
from document_loader import load_documents
from information_retriever import retrieve_information
from decision_evaluator import evaluate_decision
from response_formatter import format_response

app = Flask(__name__)
CORS(app)

# Global variables to store documents and the LLM pipeline.
documents = []
loading_error = None

def load_all_resources():
    """
    Function to load all resources (documents and model) in a controlled way.
    This will be called only once when the server starts.
    """
    global documents, loading_error
    try:
        print("Loading documents...")
        docs_dir_path = os.path.join(os.getcwd(), 'LLM_Document_Processing_System', 'documents')
        documents = load_documents(docs_dir_path)
        
        if not documents:
            print("WARNING: No documents found. This will cause rejections.")
        
        print("Application resources loaded successfully.")
    except Exception as e:
        loading_error = f"Failed to load resources: {e}"
        print(f"FATAL LOADING ERROR: {loading_error}")
        traceback.print_exc()

@app.route('/')
def index():
    return "The server is running. Please use the frontend UI to interact with it."

@app.route('/evaluate_query', methods=['POST'])
def evaluate_query():
    global documents
    if loading_error:
        # If there was a loading error at startup, return it to the UI
        return jsonify({"error": f"Server failed to initialize resources. Details: {loading_error}"}), 500

    if not documents:
        return jsonify({
            "error": "No documents found. Please add PDF or DOCX files to the 'documents' directory."
        }), 500

    data = request.json
    user_query = data.get('query')

    if not user_query:
        return jsonify({"error": "No query provided."}), 400

    try:
        parsed_query = parse_query(user_query)
        # The retrieve_information function now makes the API call directly.
        retrieved_info = retrieve_information(parsed_query['procedure'], documents)
        decision, amount, justification = evaluate_decision(retrieved_info)
        response = format_response(decision, amount, justification)
        
        return jsonify(json.loads(response)), 200
    except ValueError as e:
        return jsonify({"error": f"Invalid query format. {str(e)}"}), 400
    except Exception as e:
        print("An unhandled exception occurred during query evaluation:")
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred. Please check the server logs for details."}), 500

if __name__ == '__main__':
    # Load resources before starting the server
    load_all_resources()

    docs_dir_path = os.path.join(os.getcwd(), 'LLM_Document_Processing_System', 'documents')
    if not os.path.exists(docs_dir_path):
        os.makedirs(docs_dir_path)
        print(f"Created directory '{docs_dir_path}'. Please place your policy documents inside.")
    
    app.run(debug=True, port=5000)


