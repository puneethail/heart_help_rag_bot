# 🫀 Heart Help RAG Bot

A Retrieval-Augmented Generation (RAG) chatbot designed to provide heart health information and assistance using advanced language models and vector databases.

## 📋 Overview

This project implements a RAG-based chatbot that leverages ChromaDB for vector storage and retrieval to answer questions related to heart health. The system combines the power of large language models (Google Gemini) with efficient document retrieval to provide accurate and contextual responses.

## 🗂️ Project Structure

```
heart_help_rag_bot/
├── .gitignore
├── README.md
├── requirements.txt
├── test.ipynb
├── test.py
├── test_frontend.py
├── chroma_db/
└── src/
    ├── backend/
    ├── constants/
    ├── docs/
    └── notebooks/
```

## 🛠️ Technologies Used

- **Primary Language**: Jupyter Notebook (80.5%), Python (19.5%)
- **Vector Database**: ChromaDB v1.2.0
- **LLM Framework**: LangChain v1.0.1
- **AI Models**: Google Generative AI (Gemini)
- **Frontend**: Gradio v5.49.1
- **Document Processing**: PyMuPDF v1.26.5

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/puneethail/heart_help_rag_bot.git
cd heart_help_rag_bot
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 🔑 Configuration

1. Create a `.env` file in the root directory:
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

2. Obtain your Google API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 📚 Dependencies

```txt
chromadb==1.2.0
google-genai==1.45.0
gradio==5.49.1
langchain==1.0.1
langchain-chroma==1.0.0
langchain-classic==1.0.0
langchain-community==0.4
langchain-core==1.0.0
langchain-google-genai==2.1.12
langchain-google-vertexai==2.1.2
langchain-openai==1.0.0
langchain-text-splitters==1.0.0
numpy==2.2.6
openai==2.5.0
pandas==2.3.3
PyMuPDF==1.26.5
python-dotenv==1.1.1
regex==2025.9.18
```

## 🚀 Usage

### Running the CLI Backend Test

```bash
python test.py
```

**Example interaction:**
```
You: What are the symptoms of heart disease?
Assistant: [Response with relevant heart health information]

You: exit
Assistant: Thank you for the conversation! If you have any more questions in the future, feel free to ask.
```

### Running the Frontend with Gradio

```bash
python test_frontend.py
```

This will launch a web interface where you can interact with the chatbot through your browser.

### Using Jupyter Notebook

```bash
jupyter notebook test.ipynb
```

Open the notebook in your browser to interactively test and develop features.

## 🧠 Key Features

- **RAG Architecture**: Combines vector search with generative AI for accurate responses
- **Conversation History**: Maintains context across multiple exchanges
- **ChromaDB Integration**: Efficient vector storage and similarity search
- **Multiple Interfaces**: CLI, Web UI (Gradio), and Jupyter notebook
- **Document Processing**: PDF parsing capabilities with PyMuPDF
- **LangChain Integration**: Modular and extensible LLM framework

## 📁 Key Components

### Backend (`src/backend/llm.py`)
Contains the main LLM class with history management:
```python
from src.backend.llm import llm

llm_ob = llm()
response = llm_ob.llm_with_history(query="Your question here")
```

### Constants (`src/constants.py`)
Configuration management including API keys and environment variables.

### Vector Database (`chroma_db/`)
Stores document embeddings for efficient retrieval during query processing.

## 🔄 How It Works

1. **Document Ingestion**: Heart health documents are processed and converted to embeddings
2. **Vector Storage**: Embeddings are stored in ChromaDB for fast retrieval
3. **Query Processing**: User queries are embedded and similar documents are retrieved
4. **Response Generation**: Retrieved context is combined with the query and sent to the LLM
5. **History Management**: Conversation history is maintained for contextual responses

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/puneethail/heart_help_rag_bot/issues).

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is available for educational and research purposes.

## 👤 Author

**Puneeth Ail**
- GitHub: [@puneethail](https://github.com/puneethail)
- Repository: [heart_help_rag_bot](https://github.com/puneethail/heart_help_rag_bot)

## ⚠️ Disclaimer

This chatbot is designed for informational purposes only and should not be considered as medical advice. Always consult with qualified healthcare professionals for medical concerns.

## ⭐ Show your support

Give a ⭐️ if this project helped you!

---

