from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class DocumentResponse(BaseModel):
    id: int = Field(
        ...,
        description="Unique ID of the uploaded document"
    )

    filename: str = Field(
        ...,
        description="Original name of the uploaded document"
    )

    file_type: str = Field(
        ...,
        description="File extension of the document"
    )

    created_at: datetime = Field(
        ...,
        description="Date and time when the document was uploaded"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 5,
                "filename": "employee.txt",
                "file_type": ".txt",
                "created_at": "2026-07-17T11:19:09.847381+05:30"
            }
        }
    )