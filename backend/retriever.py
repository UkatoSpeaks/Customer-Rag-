from langchain_chroma import Chroma

from config import embeddings, CHROMA_DB_DIR


vector_store = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embeddings,
)


retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


def retrieve_documents(query: str):
    return retriever.invoke(query)


def format_documents(documents):
    return "\n\n".join(doc.page_content for doc in documents)