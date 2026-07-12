import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ingest import ingest
from rag_chain import ask_question
from schemas import ChatRequest, ChatResponse

DB_PATH = "db"

# Create vector database automatically if it doesn't exist
if not os.path.exists(DB_PATH):
    print("Vector database not found. Creating...")
    ingest()
    print("Vector database created successfully!")

app = FastAPI(
    title="GigaCorp Customer Support API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "GigaCorp Customer Support API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    response = ask_question(
        question=request.question,
        session_id=request.session_id,
    )

    return ChatResponse(
        answer=response["answer"],
        sources=response["sources"],
    )