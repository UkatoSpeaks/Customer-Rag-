from langchain_chroma import Chroma

from config import embeddings, CHROMA_DB_DIR


def get_retriever():
    vector_store = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings,
    )

    return vector_store.as_retriever(
        search_kwargs={"k": 3}
    )


def retrieve_documents(query: str):
    retriever = get_retriever()

    docs = retriever.invoke(query)

    print("=" * 60)
    print("Query:", query)
    print("Retrieved documents:", len(docs))

    for i, doc in enumerate(docs):
        print(f"\nDocument {i + 1}:")
        print(doc.page_content[:300])
        print(doc.metadata)

    print("=" * 60)

    return docs


def format_documents(documents):
    return "\n\n".join(
        doc.page_content
        for doc in documents
    )