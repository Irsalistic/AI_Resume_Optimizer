import logging
import os
import fitz
from dotenv import load_dotenv

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from docx import Document
import prompts
from langchain.llms import Ollama
import os

from groq import Groq


def get_file_extension(uploaded_file):
    # Extract the file extension from the uploaded file's name
    _, ext = os.path.splitext(uploaded_file.name)
    if ext:
        return ext[1:].lower()  # Remove the dot and convert to lower case
    return None


def get_resume_text(uploaded_file):
    result = None
    file_extension = get_file_extension(uploaded_file)
    logging.info(f"Detected file extension: {file_extension}")

    if file_extension == 'pdf':
        result = extract_text_from_pdf(uploaded_file)
    elif file_extension == 'docx':
        result = extract_text_from_docx(uploaded_file)
    else:
        logging.error(f"Unsupported file format: {file_extension}")
        return ""

    logging.info(f"Extracted resume text length: {len(result)}")
    return result


def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
    except Exception as e:
        logging.error(f"Error reading PDF file: {e}")
    if not text.strip():
        logging.warning("Extracted text from PDF is empty.")
    return text


def extract_text_from_docx(uploaded_file):
    resume_text = ""
    try:
        doc = Document(uploaded_file)
        for paragraph in doc.paragraphs:
            resume_text += paragraph.text + "\n"
    except Exception as e:
        logging.error(f"Error reading DOCX file: {e}")
    return resume_text


def main():
    load_dotenv()

    st.set_page_config(page_title="Improve your resume")
    st.header("Resume Optimization")
    company = st.text_input("Which company are you applying for?")
    role = st.text_input("What role are you applying for?")
    job_description = st.text_input("Enter the job description here:")

    resume = st.file_uploader("Upload your resume here", type=["docx", "pdf"])
    if st.button("Go"):
        if not (company and role and job_description and resume):
            st.error("Please fill in all the fields")
            st.stop()
        with st.spinner("Loading..."):
            # get resume text
            resume_text = get_resume_text(resume)

            # chat_gpt = ChatOpenAI(temperature=0.9, model_name="gpt-4")
            llm = Ollama(temperature=0.8, model="llama3.1:8b")
            memory = ConversationBufferMemory()
            chain = ConversationChain(llm=llm, memory=memory, verbose=True)
            response = chain.predict(
                input=prompts.PROMPT.format(job_description=job_description, role=role, company=company,
                                            resume=resume_text))
            st.write(response)


if __name__ == "__main__":
    main()
