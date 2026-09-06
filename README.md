# Resume Optimizer

A Streamlit app that reads your resume (PDF or DOCX), compares it to a job description, and suggests improvements with an LLM.

Works with **Ollama** (local), **OpenAI**, or **Groq**.

## Features

- Upload a resume as PDF or DOCX
- Paste a company, role, and job description
- Tailored rewrite suggestions from the model you configure

## Setup

```bash
git clone https://github.com/Irsalistic/AI_Resume_Optimizer.git
cd AI_Resume_Optimizer
pip install -r requirements.txt
```

Optional `.env` for cloud providers:

```env
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
```

Set `LLM_PROVIDER` to `ollama` (default), `openai`, or `groq`. Local Ollama does not need API keys. Install [Ollama](https://ollama.com/) and pull a model such as `llama3.1:8b`.

## Run

```bash
streamlit run app.py
```

Open http://localhost:8501, fill in the company and role, upload the resume, and click **Go**.

## Layout

```
app.py              # Streamlit UI and LLM calls
prompts.py          # Prompt templates
requirements.txt
```
