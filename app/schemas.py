from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str


class Source(BaseModel):
    id: str
    filename: str | None = None
    chunk_index: int | None = None
    score: float | None = None


class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]