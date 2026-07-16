from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class SourceReference(BaseModel):
    filename: str
    chunk_index: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceReference]