# document_loader.py
import os
from pdfminer.high_level import extract_text
from docx import Document

def load_documents(directory):
    """
    Loads text from all .pdf and .docx files in a given directory.

    Args:
        directory (str): The path to the directory containing documents.

    Returns:
        list: A list of strings, where each string is the text content of a document.
    """
    documents = []
    # Check if the directory exists and is not empty
    if not os.path.isdir(directory):
        # Create a directory if it doesn't exist
        os.makedirs(directory)
        print(f"Directory '{directory}' created. Please add your documents to it.")
        return documents

    file_list = os.listdir(directory)
    if not file_list:
        print(f"No files found in directory: {directory}")
        return documents

    for filename in file_list:
        file_path = os.path.join(directory, filename)
        # Skip directories
        if os.path.isdir(file_path):
            continue

        try:
            if filename.endswith('.pdf'):
                # Extract text from a PDF file
                text = extract_text(file_path)
                documents.append(text)
                print(f"Loaded {filename} successfully.")
            elif filename.endswith('.docx'):
                # Extract text from a DOCX file
                doc = Document(file_path)
                text = '\n'.join([para.text for para in doc.paragraphs])
                documents.append(text)
                print(f"Loaded {filename} successfully.")
            else:
                print(f"Skipping {filename}: Not a .pdf or .docx file.")
        except ImportError as e:
            # Catch specific import errors to identify missing libraries
            print(f"FATAL ERROR: A required library is not installed for file {filename}. Details: {e}")
            raise  # Re-raise the exception to stop the program
        except Exception as e:
            # Print a detailed error message for files that fail to load
            print(f"Warning: Could not process {filename}. Error: {e}")
    return documents
