# Resume Screening
The Resume Screening App is a simple tool that uses Natural Language Processing (NLP) to match job descriptions with resumes. It assists in quickly filtering and ranking resumes based on their similarity to a given job description, making the hiring process more efficient.

Web app : https://newchakri-resume-screening.streamlit.app

![image](https://i.postimg.cc/k4KTBD7c/Resume-screening-app.jpg)


# Features
**Flexible Input**: The app supports various input methods for job descriptions, including plain text input and file upload (PDF or TXT). You can also upload multiple resumes in PDF format.

**Efficient Screening**: The app uses Sentence-BERT (BERT-based NLP model) for text embeddings and calculates cosine similarity scores to measure how closely each resume matches the job description.

**Ranked Resumes**: Resumes are ranked in real-time based on their similarity scores, enabling you to focus on candidates who are the best match for the position.

**Interactive User Interface**: The Streamlit-powered user interface allows users to interact with the app seamlessly. Setting the job description, uploading resumes, and ranking candidates is a breeze.

# Technical Details
**Python**: The app is primarily built using Python, a versatile programming language known for its extensive libraries and community support.

**PDF Parsing**: The app employs the PyMuPDF (fitz) library to extract text from PDF files, ensuring compatibility with common resume formats.

**Text Preprocessing**: Resumes and job descriptions undergo text preprocessing, including the removal of stopwords, punctuation, and special characters.

**Sentence-BERT**: The app uses Sentence-BERT, a BERT-based NLP model, for text embeddings and cosine similarity calculations.

**Streamlit**: The user interface is developed using Streamlit, a Python library for creating web applications with minimal effort.








