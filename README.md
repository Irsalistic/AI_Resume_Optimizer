# Resume Optimization Tool

A Streamlit-based application that helps users optimize their resumes for specific job applications using Language Learning Models (LLMs). The tool analyzes your resume against job descriptions and provides tailored recommendations.

## Features

- Upload resume in PDF or DOCX format
- Process job descriptions
- Company and role-specific optimization
- Integration with multiple LLM options (Ollama, OpenAI, Groq)
- Real-time resume analysis and feedback
- User-friendly Streamlit interface

## Prerequisites

- Python 3.8+
- Streamlit
- PyMuPDF (fitz)
- python-docx
- langchain
- python-dotenv
- Ollama

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd resume-optimizer
```

2. Install required dependencies:
```bash
pip install streamlit pymupdf python-docx langchain python-dotenv
```

3. Set up environment variables in `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Access the application through your web browser (typically http://localhost:8501)

3. Fill in the required information:
   - Target company name
   - Role you're applying for
   - Job description
   - Upload your resume (PDF or DOCX format)

4. Click "Go" to receive optimization suggestions

## File Structure

```
project/
├── main.py              # Main application file
├── prompts.py          # LLM prompt templates
├── .env               # Environment variables
└── requirements.txt    # Project dependencies
```

## Supported File Formats

- PDF (.pdf)
- Microsoft Word (.docx)

## Features in Detail

### Resume Text Extraction
- Automatic detection of file format
- PDF text extraction using PyMuPDF
- DOCX parsing using python-docx
- Error handling for file processing

### LLM Integration
- Default configuration with Ollama (llama3.1:8b)
- Configurable temperature for response variation
- Conversation memory buffer for context maintenance
- Support for multiple LLM providers (OpenAI, Groq)

### User Interface
- Clean and intuitive Streamlit interface
- Real-time feedback
- Error handling for missing inputs
- Loading indicators for processing status

## Error Handling

The application includes comprehensive error handling for:
- Invalid file formats
- Empty or corrupted files
- Missing input fields
- API connection issues


## Acknowledgments

- Built with Streamlit
- Powered by Langchain
- Uses Ollama LLM

## Future Enhancements

- Additional file format support
- Enhanced analysis capabilities
- Custom prompt templates
- Batch processing support
