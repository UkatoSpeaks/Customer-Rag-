import os

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings

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

CHROMA_DB_DIR = "db/chroma"