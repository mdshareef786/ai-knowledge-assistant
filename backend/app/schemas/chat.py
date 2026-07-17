from pydantic import BaseModel, Field, ConfigDict


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Question to ask based on the uploaded documents"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "question about the uploaded documents"
            }
        }
    )


class SourceReference(BaseModel):
    filename: str = Field(
        ...,
        description="Name of the source document"
    )

    chunk_index: int = Field(
        ...,
        description="Index of the relevant document chunk"
    )


class ChatResponse(BaseModel):
    answer: str = Field(
        ...,
        description="AI-generated answer based on uploaded documents"
    )

    sources: list[SourceReference] = Field(
        default_factory=list,
        description="Document sources used to generate the answer"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "answer": "The notice period is 60 days.",
                "sources": [
                    {
                        "filename": "employee.txt",
                        "chunk_index": 0
                    }
                ]
            }
        }
    )