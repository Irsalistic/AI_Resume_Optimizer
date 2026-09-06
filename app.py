import logging
import os

import fitz
import streamlit as st
from dotenv import load_dotenv
from docx import Document

import prompts

load_dotenv()


def get_file_extension(uploaded_file):
    _, ext = os.path.splitext(uploaded_file.name)
    return ext[1:].lower() if ext else None


def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
    except Exception as exc:
        logging.error("Error reading PDF file: %s", exc)
    if not text.strip():
        logging.warning("Extracted text from PDF is empty.")
    return text


def extract_text_from_docx(uploaded_file):
    resume_text = ""
    try:
        doc = Document(uploaded_file)
        for paragraph in doc.paragraphs:
            resume_text += paragraph.text + "\n"
    except Exception as exc:
        logging.error("Error reading DOCX file: %s", exc)
    return resume_text


def get_resume_text(uploaded_file):
    file_extension = get_file_extension(uploaded_file)
    if file_extension == "pdf":
        return extract_text_from_pdf(uploaded_file)
    if file_extension == "docx":
        return extract_text_from_docx(uploaded_file)
    logging.error("Unsupported file format: %s", file_extension)
    return ""


def build_llm():
    provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
    if provider == "openai":
        from langchain_community.chat_models import ChatOpenAI

        return ChatOpenAI(temperature=0.8, model_name=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    if provider == "groq":
        from langchain_groq import ChatGroq

        return ChatGroq(temperature=0.8, model_name=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"))
    from langchain_community.llms import Ollama

    return Ollama(temperature=0.8, model=os.getenv("OLLAMA_MODEL", "llama3.1:8b"))


def main():
    st.set_page_config(page_title="Improve your resume")
    st.header("Resume Optimization")
    company = st.text_input("Which company are you applying for?")
    role = st.text_input("What role are you applying for?")
    job_description = st.text_area("Enter the job description here:")
    resume = st.file_uploader("Upload your resume here", type=["docx", "pdf"])

    if not st.button("Go"):
        return
    if not (company and role and job_description and resume):
        st.error("Please fill in all the fields")
        return

    with st.spinner("Loading..."):
        resume_text = get_resume_text(resume)
        if not resume_text.strip():
            st.error("Could not read text from that resume.")
            return
        from langchain.chains import ConversationChain
        from langchain.memory import ConversationBufferMemory

        chain = ConversationChain(llm=build_llm(), memory=ConversationBufferMemory(), verbose=False)
        response = chain.predict(
            input=prompts.PROMPT.format(
                job_description=job_description,
                role=role,
                company=company,
                resume=resume_text,
            )
        )
        st.write(response)


if __name__ == "__main__":
    main()
