import io
import fitz
import re
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

# Function to preprocess text
def preprocess_text(text):
    text = text.replace("\n", " ")
    text = text.replace("- ", " ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Create a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

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
    for uploaded_resume in uploaded_resumes:
        resume_text = extract_text_from_pdf(uploaded_resume)
        if resume_text:
            resume_text = preprocess_text(resume_text)

            job_description_tfidf = tfidf_vectorizer.fit_transform([job_description_text])
            similarities = cosine_similarity(job_description_tfidf, tfidf_vectorizer.transform([resume_text]))

            score = similarities[0][0]

            # Convert similarity score to a percentage
            percentage_match = score * 100

            # Store the percentage match for this resume
            similarity_scores[uploaded_resume.name] = percentage_match

    # Display ranked resumes with percentage match
    sorted_resumes = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

    st.subheader("Ranked Resumes:")
    for rank, (resume_name, percentage_match) in enumerate(sorted_resumes, start=1):
        st.write(f"Rank {rank}: {resume_name}, Match Percentage: {percentage_match:.2f}%")
