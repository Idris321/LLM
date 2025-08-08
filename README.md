# **Insurance Claim Evaluator**

An automated system to review and evaluate medical claims against policy documents using a generative AI. This project demonstrates how to build a web-based application that processes natural language queries and provides instant, justified decisions.

## **Project Overview**

The application functions as a claim processing tool. A user inputs a query with details of a medical procedure (e.g., "knee replacement"). The system then analyzes a set of insurance policy documents to determine if the claim is valid based on coverage, exclusions, or waiting periods. The result is a clear decision (Approved or Rejected) with a justification extracted from the policy text.

## **Technical Stack**

* **Backend:** Python with Flask  
* **Frontend:** HTML, CSS (Tailwind CSS), and JavaScript  
* **AI Integration:** Gemini API for document analysis  
* **Document Processing:** pdfminer.six for PDFs and python-docx for Word files

## **Getting Started**

Follow these steps to set up and run the project on your local machine.

### **1\. Prerequisites**

* Python 3.8 or higher  
* pip (Python package installer)  
* A Gemini API key

### **2\. Setup**

#### **Clone the Repository**

git clone \<your-repository-url\>  
cd \<your-repository-folder\>

#### **Create and Activate a Virtual Environment**

It is highly recommended to use a virtual environment to manage dependencies.

python \-m venv venv  
venv\\Scripts\\activate  \# On Windows  
\# source venv/bin/activate  \# On macOS/Linux

#### **Install Dependencies**

Install all the required Python libraries using the requirements.txt file.

pip install \-r requirements.txt

### **3\. Configuration**

#### **Securely Store Your API Key**

Hardcoding API keys is a security risk. This project uses a .env file to manage secrets.

1. Create a file named .env in the root of your project directory.  
2. Add your Gemini API key to this file in the following format:  
   GEMINI\_API\_KEY=YOUR\_ACTUAL\_API\_KEY\_HERE

3. Ensure your .gitignore file includes .env to prevent accidentally committing your key to GitHub.

### **4\. How to Use**

#### **Place Policy Documents**

Put all your policy documents (PDF and DOCX files) into the LLM\_Document\_Processing\_System/documents directory. The application will load these files at startup.

#### **Run the Flask Server**

Start the backend server from your terminal.

python app.py

The server will load the documents and the Gemini API pipeline. You should see a message indicating that the application is running on http://127.0.0.1:5000.

#### **Access the User Interface**

Open the index.html file in your web browser. This will open the frontend UI, which will communicate with your running Flask server.

The UI will provide an input field for your query. Use the following format for your queries:  
age gender, medical procedure, location, policy duration  
Example: 65 male, deep brain stimulation, Pune, 1 year

## **Sample Queries**

Here are some test queries to validate the application's functionality:

### **Approved Claims**

* 65 male, deep brain stimulation, Pune, 1 year  
* 40 female, Oral chemotherapy, Delhi, 3 years

### **Rejected Claims**

* 30 male, hernia, Hyderabad, 1 year  
* 25 male, cosmetic surgery, Bangalore, 2 years