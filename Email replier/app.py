import os
import logging
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document
import extract_msg
from dotenv import load_dotenv
import openai

# Configure logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

openai.api_type = "azure"
openai.api_base = os.environ["AZURE_OPENAI_ENDPOINT"]
openai.api_version = os.environ["AZURE_OPENAI_API_VERSION"]
openai.api_key = os.environ["AZURE_OPENAI_API_KEY"]

ALLOWED_EXTENSIONS = {'msg', 'pdf', 'txt', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_question(line):
    question_words = ['what', 'how', 'why', 'who', 'where', 'when', 'which']
    return any(line.lower().startswith(word) for word in question_words)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_file', methods=['POST'])
def process_file():
    logging.debug('Process file endpoint called')
    if 'file' not in request.files:
        logging.error('No file part in the request')
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        logging.error('No selected file')
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        logging.debug(f'File saved to {filepath}')

        file_ext = filename.rsplit('.', 1)[1].lower()
        if file_ext == 'msg':
            text = extract_msg_content(filepath)
        elif file_ext == 'pdf':
            text = extract_pdf_content(filepath)
        elif file_ext == 'txt':
            text = extract_txt_content(filepath)
        elif file_ext == 'docx':
            text = extract_docx_content(filepath)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        logging.debug(f'Extracted text: {text[:500]}...')  # Log only the first 500 characters

        # Detect questions in the text
        questions = [line.strip() for line in text.split('\n') if is_question(line.strip())]
        logging.debug(f'Extracted questions: {questions}')

        # If no questions are found, create a default question for the entire text
        if not questions:
            questions = [f"What is the content of this document?"]

        # Generate answers using OpenAI model
        answers = []
        for question in questions:
            prompt = f"Answer the following question briefly and concisely:\n\n{question}"
            try:
                logging.debug(f'Prompt: {prompt}')
                response = openai.Completion.create(
                    engine="gpt-35-turbo",  # Use your actual deployment name
                    prompt=prompt,
                    max_tokens=100,  # Limit response length
                    stop=None
                )
                answer = response.choices[0].text.strip()
                logging.debug(f'Answer: {answer}')
                answers.append({'question': question, 'answer': answer})
            except openai.error.InvalidRequestError as e:
                logging.error(f'Error from OpenAI: {e}')
                return jsonify({'error': str(e)}), 500

        logging.debug(f'Generated answers: {answers}')
        return jsonify({'answers': answers})

def extract_msg_content(filepath):
    msg = extract_msg.Message(filepath)
    return msg.body

def extract_pdf_content(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_txt_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def extract_docx_content(filepath):
    doc = Document(filepath)
    return '\n'.join([para.text for para in doc.paragraphs])

if __name__ == '__main__':
    app.run(debug=True)
