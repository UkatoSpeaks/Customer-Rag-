# GigaCorp AI Customer Support (RAG)

An AI-powered customer support assistant that answers customer queries using a company knowledge base. The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from a PDF before generating responses with Mistral AI.

The project consists of a FastAPI backend for handling RAG and a Streamlit frontend for interacting with the chatbot.

---

## Demo

### Live Frontend

https://owqmmwdpszehh77vybjqpe.streamlit.app/

### Live Backend API

https://customer-rag-2.onrender.com

### API Documentation

https://customer-rag-2.onrender.com/docs

---

## Features

- AI-powered customer support chatbot
- Retrieval-Augmented Generation (RAG)
- Conversational memory for follow-up questions
- Query rewriting for context-aware conversations
- PDF-based knowledge base
- Chroma vector database
- Mistral AI embeddings and LLM
- Source citation for every response
- FastAPI REST API
- Streamlit user interface
- Fully deployed on Render and Streamlit Community Cloud

---

## Tech Stack

### Backend

- Python
- FastAPI
- LangChain
- ChromaDB
- Mistral AI
- PyPDF
- Uvicorn

### Frontend

- Streamlit
- Requests

### AI Components

- Mistral Small
- Mistral Embeddings
- Retrieval-Augmented Generation (RAG)
- Conversational Memory

---

## Project Structure

```
Customer-Rag/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── ingest.py
│   ├── rag_chain.py
│   ├── retriever.py
│   ├── prompts.py
│   ├── memory.py
│   ├── schemas.py
│   ├── data/
│   │   └── gigacorp_faq.pdf
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   └── requirements.txt
│
└── README.md
```

---

## How It Works

1. The PDF knowledge base is loaded.
2. The document is split into smaller chunks.
3. Each chunk is converted into vector embeddings using Mistral Embeddings.
4. The embeddings are stored in ChromaDB.
5. When a user asks a question:
   - The question is rewritten if it's a follow-up.
   - Relevant chunks are retrieved from ChromaDB.
   - The retrieved context is sent to the LLM.
   - The assistant generates an answer based only on the retrieved information.
6. The conversation history is stored to support follow-up questions.

---

## Running Locally

### Clone the repository

```bash
git clone https://github.com/UkatoSpeaks/Customer-Rag-.git

cd Customer-Rag
```

---

### Backend

```bash
cd backend

pip install -r requirements.txt
```

Create a `.env` file.

```env
MISTRAL_API_KEY=your_api_key
```

Create the vector database.

```bash
python ingest.py
```

Start the backend.

```bash
uvicorn app:app --reload
```

---

### Frontend

Open another terminal.

```bash
cd frontend

pip install -r requirements.txt

streamlit run app.py
```

---

## API Endpoint

### POST `/chat`

Example Request

```json
{
  "question": "Do you ship to India?",
  "session_id": "user1"
}
```

Example Response

```json
{
  "answer": "Yes, GigaCorp ships to India. Shipping costs depend on the destination and delivery option.",
  "sources": [
    {
      "source": "gigacorp_faq",
      "page": 2
    }
  ]
}
```

---

## Sample Questions

- Do you ship to India?
- What are your business hours?
- What is your refund policy?
- How can I contact support?
- Do you offer premium plans?
- How do I reset my password?

---

## Screenshots

You can add screenshots here after deployment.

### Home Page

```
images/home.png
```

### Chat Interface

```
images/chat.png
```

### API Documentation

```
images/swagger.png
```

---

## Future Improvements

- Upload custom PDFs from the UI
- Support multiple knowledge bases
- Streaming responses
- Authentication
- Chat history persistence
- Admin dashboard
- Analytics for frequently asked questions
- Docker support
- Multi-language support

---

## Author

**Anurag Chaudhary**

GitHub:
https://github.com/UkatoSpeaks

Portfolio:
https://finalp-gray.vercel.app/

---

## License

This project is intended for learning and portfolio purposes.
