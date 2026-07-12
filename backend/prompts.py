from langchain_core.prompts import ChatPromptTemplate


REWRITE_PROMPT = ChatPromptTemplate.from_template(
    """
You are an AI assistant.

Given the previous conversation and the latest user question,
rewrite the latest question into a complete standalone question.

If the latest question is already complete,
return it unchanged.

Conversation History:
{history}

Latest Question:
{question}

Standalone Question:
"""
)


SUPPORT_PROMPT = ChatPromptTemplate.from_template(
    """
You are GigaCorp's AI customer support assistant.

Answer ONLY using the provided context.

Rules:
- Use only the provided context.
- If the answer is not available, reply:
"I couldn't find that information in the knowledge base."
- Be concise and helpful.
- NEVER mention document names, PDF names, file names, or source names in your answer.

Conversation History:
{history}

Context:
{context}

Question:
{question}
"""
)