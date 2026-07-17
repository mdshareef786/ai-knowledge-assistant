from typing import Generic, TypeVar

from pydantic import BaseModel, Field, ConfigDict


T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool = Field(
        ...,
        description="Indicates whether the request was successful."
    )

    message: str = Field(
        ...,
        description="Human-readable response message."
    )

    data: T | None = Field(
        default=None,
        description="Response payload."
    )

    errors: dict | list | None = Field(
        default=None,
        description="Validation or business errors."
    )

    meta: dict | None = Field(
        default=None,
        description="Additional metadata such as pagination."
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Request completed successfully.",
                "data": {},
                "errors": None,
                "meta": None
            }
        }
    )