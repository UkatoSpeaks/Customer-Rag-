import os

from langchain_core.output_parsers import StrOutputParser

from config import llm
from memory import memory
from prompts import REWRITE_PROMPT, SUPPORT_PROMPT
from retriever import retrieve_documents, format_documents


parser = StrOutputParser()


def rewrite_question(question: str, history: str) -> str:
    chain = REWRITE_PROMPT | llm | parser

    return chain.invoke(
        {
            "history": history,
            "question": question,
        }
    )


def ask_question(question: str, session_id: str = "default"):
    history = memory.get_history(session_id)

    standalone_question = rewrite_question(
        question,
        history,
    )

    docs = retrieve_documents(
        standalone_question,
    )

    context = format_documents(docs)

    answer_chain = SUPPORT_PROMPT | llm | parser

    answer = answer_chain.invoke(
        {
            "history": history,
            "context": context,
            "question": question,
        }
    )

    memory.add_message(
        session_id,
        "user",
        question,
    )

    memory.add_message(
        session_id,
        "assistant",
        answer,
    )

    sources = []
    seen = set()

    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        # Show only clean filename without path or extension
        source = os.path.splitext(os.path.basename(source))[0]
        page = doc.metadata.get("page", 0) + 1

        key = (source, page)

        if key not in seen:
            seen.add(key)

            sources.append(
                {
                    "source": source,
                    "page": page,
                }
            )

    return {
        "answer": answer,
        "sources": sources,
    }