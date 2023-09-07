import io
import fitz
import re
import streamlit as st
from sentence_transformers import SentenceTransformer, util

# Function to preprocess and extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        # Open the PDF file using fitz.Document and io.BytesIO
        with io.BytesIO(pdf_file.read()) as pdf_buffer:
            pdf_document = fitz.open("pdf", pdf_buffer.read())

        # Determine the number of pages in the PDF document
        num_pages = len(pdf_document)

        # Extract text from each page
        for page_num in range(num_pages):
            page = pdf_document[page_num]
            text += page.get_text()
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
    return text

# Create a Sentence-BERT model
sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')

# Streamlit app
st.title("📄 Resume Screening App")

# Radio button for choosing input method for job description
job_description_input_method = st.radio("Choose Job Description Input Method:", ("Text", "Upload File"))

# Initialize job description text
job_description_text = ""

# Handle job description input based on the chosen method
if job_description_input_method == "Text":
    job_description_text = st.text_area("Enter the job description", "")
else:
    uploaded_job_description = st.file_uploader("Upload a job description PDF or TXT file:", type=["pdf", "txt"])

    if uploaded_job_description is not None:
        if uploaded_job_description.type == "text/plain":
            # Read the plain text input
            job_description_text = uploaded_job_description.read().decode("utf-8")
        elif uploaded_job_description.type == "application/pdf":
            # Extract text from the PDF input
            job_description_text = extract_text_from_pdf(uploaded_job_description)

if st.button("Set Job Description") and job_description_text:
    st.success("Job description text set successfully.")

# Upload resumes
uploaded_resumes = st.file_uploader("Upload resume PDF files:", type=["pdf"], accept_multiple_files=True)

# Calculate similarity scores when both job description and resumes are provided
if st.button("Rank Resumes") and (job_description_text or uploaded_resumes is not None):
    similarity_scores = {}
    
    # Encode the job description text
    job_description_embedding = sbert_model.encode(job_description_text, convert_to_tensor=True)
    
    for uploaded_resume in uploaded_resumes:
        resume_text = extract_text_from_pdf(uploaded_resume)
        if resume_text:
            resume_text = preprocess_text(resume_text)
            
            # Encode the resume text
            resume_embedding = sbert_model.encode(resume_text, convert_to_tensor=True)

            # Calculate cosine similarity
            similarity_score = util.pytorch_cos_sim(job_description_embedding, resume_embedding)

            # Convert similarity score to a percentage
            percentage_match = similarity_score.item() * 100

            # Store the percentage match for this resume
            similarity_scores[uploaded_resume.name] = percentage_match

    # Display ranked resumes with percentage match
    sorted_resumes = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

    st.subheader("Ranked Resumes:")
    for rank, (resume_name, percentage_match) in enumerate(sorted_resumes, start=1):
        st.write(f"Rank {rank}: {resume_name}, Match Percentage: {percentage_match:.2f}%")
import io
import fitz
import re
import streamlit as st
from sentence_transformers import SentenceTransformer, util

# Function to preprocess and extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        # Open the PDF file using fitz.Document and io.BytesIO
        with io.BytesIO(pdf_file.read()) as pdf_buffer:
            pdf_document = fitz.open("pdf", pdf_buffer.read())

        # Determine the number of pages in the PDF document
        num_pages = len(pdf_document)

        # Extract text from each page
        for page_num in range(num_pages):
            page = pdf_document[page_num]
            text += page.get_text()
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
    return text

# Create a Sentence-BERT model
sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')

# Streamlit app
st.title("📄 Resume Screening App")

# Radio button for choosing input method for job description
job_description_input_method = st.radio("Choose Job Description Input Method:", ("Text", "Upload File"))

# Initialize job description text
job_description_text = ""

# Handle job description input based on the chosen method
if job_description_input_method == "Text":
    job_description_text = st.text_area("Enter the job description", "")
else:
    uploaded_job_description = st.file_uploader("Upload a job description PDF or TXT file:", type=["pdf", "txt"])

    if uploaded_job_description is not None:
        if uploaded_job_description.type == "text/plain":
            # Read the plain text input
            job_description_text = uploaded_job_description.read().decode("utf-8")
        elif uploaded_job_description.type == "application/pdf":
            # Extract text from the PDF input
            job_description_text = extract_text_from_pdf(uploaded_job_description)

if st.button("Set Job Description") and job_description_text:
    st.success("Job description text set successfully.")

# Upload resumes
uploaded_resumes = st.file_uploader("Upload resume PDF files:", type=["pdf"], accept_multiple_files=True)

# Calculate similarity scores when both job description and resumes are provided
if st.button("Rank Resumes") and (job_description_text or uploaded_resumes is not None):
    similarity_scores = {}
    
    # Encode the job description text
    job_description_embedding = sbert_model.encode(job_description_text, convert_to_tensor=True)
    
    for uploaded_resume in uploaded_resumes:
        resume_text = extract_text_from_pdf(uploaded_resume)
        if resume_text:
            resume_text = preprocess_text(resume_text)
            
            # Encode the resume text
            resume_embedding = sbert_model.encode(resume_text, convert_to_tensor=True)

            # Calculate cosine similarity
            similarity_score = util.pytorch_cos_sim(job_description_embedding, resume_embedding)

            # Convert similarity score to a percentage
            percentage_match = similarity_score.item() * 100

            # Store the percentage match for this resume
            similarity_scores[uploaded_resume.name] = percentage_match

    # Display ranked resumes with percentage match
    sorted_resumes = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

    st.subheader("Ranked Resumes:")
    for rank, (resume_name, percentage_match) in enumerate(sorted_resumes, start=1):
        st.write(f"Rank {rank}: {resume_name}, Match Percentage: {percentage_match:.2f}%")
