from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    session_id: str = "default"


class Source(BaseModel):
    source: str
    page: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]