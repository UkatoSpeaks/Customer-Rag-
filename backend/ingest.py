from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from config import embeddings, CHROMA_DB_DIR

PDF_PATH = "data/gigacorp_faq.pdf"


def load_documents():
    """Load the PDF document."""
    loader = PyPDFLoader(PDF_PATH)
    return loader.load()


def split_documents(documents):
    """Split the documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    return text_splitter.split_documents(documents)


def create_vector_store(chunks):
    """Create and persist the Chroma vector store."""
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR,
    )

    return vector_store


def ingest():
    documents = load_documents()

    print(f"Loaded {len(documents)} pages")

    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    create_vector_store(chunks)

    print("Vector database created successfully!")


if __name__ == "__main__":
    ingest()