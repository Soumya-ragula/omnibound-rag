from typing import Optional

from pydantic import BaseModel, Field, model_validator


class DocumentInput(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None
    source: Optional[str] = None
    brand: Optional[str] = None

    @model_validator(mode="after")
    def validate_document(self):
        if not self.url and not self.text:
            raise ValueError("Either 'url' or 'text' must be provided.")

        if self.url and self.text:
            raise ValueError("Provide either 'url' or 'text', not both.")

        return self


class IngestRequest(BaseModel):
    documents: list[DocumentInput] = Field(
        ...,
        min_length=1
    )


class IngestResponse(BaseModel):
    tenant_id: str
    documents_received: int
    message: str