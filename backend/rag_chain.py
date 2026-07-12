from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import llm, embeddings, CHROMA_DB_DIR

# Load the existing vector database
vector_store = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embeddings,
)

# Create the retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

# Prompt Template
prompt = ChatPromptTemplate.from_template(
    """
You are a helpful customer support assistant for GigaCorp.

Answer the user's question ONLY using the provided context.

If the answer is not available in the context, say:
"I couldn't find that information in the knowledge base."

Context:
{context}

Question:
{question}
"""
)

# Output parser
parser = StrOutputParser()


def format_docs(documents):
    """Convert retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in documents)


def ask_question(question: str):
    """Retrieve context and generate an answer."""

    docs = retriever.invoke(question)

    context = format_docs(docs)

    chain = prompt | llm | parser

    answer = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    sources = []

    for doc in docs:
        sources.append(
            {
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "Unknown") + 1,
            }
        )

    return {
        "answer": answer,
        "sources": sources,
    }