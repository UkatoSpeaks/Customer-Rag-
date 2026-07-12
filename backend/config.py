from pathlib import Path
import os

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings

BASE_DIR = Path(__file__).resolve().parent

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY is missing!")

llm = ChatMistralAI(
    api_key=MISTRAL_API_KEY,
    model="mistral-small-latest",
    temperature=0.2,
)

embeddings = MistralAIEmbeddings(
    api_key=MISTRAL_API_KEY,
    model="mistral-embed",
)

CHROMA_DB_DIR = str(BASE_DIR / "db" / "chroma")