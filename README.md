## Email Replier with Retrieval-Augmented Generation (RAG)
This project is a web application that leverages the power of Retrieval-Augmented Generation (RAG) to create an intelligent email replier. Users can upload .msg, .pdf, .txt, and .docx files. The application extracts text from these files, identifies questions within the text, and generates accurate and context-aware answers using OpenAI's GPT-35-turbo model.

## Features
  ->  **Multi-format File Upload:** Supports file uploads in .msg, .pdf, .txt, and .docx formats.
  ->  **Text Extraction:** Efficiently extracts text from the uploaded documents.
  ->  **Question Identification:** Identifies questions within the extracted text.
  ->  **Answer Generation:** Utilizes OpenAI's GPT-35-turbo model to generate contextually accurate answers.
  ->  **User-friendly Interface:** Displays questions and answers in a clean and easy-to-use interface.
  ->  **Context Preservation:** Maintains the context of the conversation to provide coherent and relevant responses.

## Technologies Used
->   **Python:** The core programming language used for the backend logic.
->    **Flask:** A lightweight WSGI web application framework for the backend.
->    **OpenAI GPT-35-turbo:** For generating intelligent responses.
->    **FAISS:** For efficient similarity search and clustering of dense vectors.
->   **LangChain:** For creating the chain of retrieval and generation tasks.
->    **dotenv:** For managing environment variables.
->    **Conda:** For managing the project's environment and dependencies.

## Retrieval-Augmented Generation (RAG)
This project utilizes the concept of Retrieval-Augmented Generation (RAG) to enhance the accuracy and relevance of the generated answers. RAG combines the power of retrieval (finding relevant documents) and generation (creating responses) to provide more informed and context-aware answers. The workflow is as follows:

-> **Document Loading:** The uploaded document is parsed and split into manageable chunks.
-> **Embedding Generation:** Each chunk is converted into dense vectors using Azure OpenAI Embeddings.
->  **Retrieval:** Relevant chunks are retrieved based on their similarity to the input query.
->  **Answer Generation:** The retrieved chunks are fed into the GPT-35-turbo model to generate accurate and contextually relevant answers.

## Installation
## Prerequisites
**Python 3.9 or above**
**Conda**

## Setup
Clone the repository:
git clone <repository_url>
cd email_replier

**Create and activate a Conda environment:**
conda create --name email_replier python=3.9
conda activate email_replier

**Install the required dependencies:**
pip install -r requirements.txt

## Set up environment variables:

Create a .env file in the root directory and add your Azure OpenAI endpoint and API key:
AZURE_OPENAI_ENDPOINT=https://<your-endpoint>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_API_VERSION=2024-02-15-preview

## Usage
**Run the Flask application:**
python app.py

**Open your browser and go to:**
http://127.0.0.1:5000/

**Upload a supported file:**

Click on the "Choose file" button and select a .msg, .pdf, .txt, or .docx file from your computer. The application will process the file, extract text, identify questions, and generate answers which will be displayed on the interface.
email_replier/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── uploads/
└── .env

## Contributing
Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.
