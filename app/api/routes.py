from fastapi import APIRouter, HTTPException

from app.models.schemas import IngestRequest, IngestResponse
from app.services.ingestion import (
    extract_text_from_url,
    clean_text,
)
from app.services.retrieval import chunk_text


router = APIRouter()


@router.post(
    "/tenants/{tenant_id}/ingest",
    response_model=IngestResponse,
)
async def ingest_documents(
    tenant_id: str,
    request: IngestRequest,
):
    processed_documents = 0
    total_chunks = 0

    for document in request.documents:

        # 1. Get the document text
        if document.text:
            raw_text = document.text

        elif document.url:
            try:
                raw_text = await extract_text_from_url(document.url)
            except Exception as exc:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to fetch URL: {document.url}"
                ) from exc

        else:
            raise HTTPException(
                status_code=400,
                detail="Document must contain either text or url."
            )

        # 2. Clean the text
        cleaned_text = clean_text(raw_text)

        if not cleaned_text:
            raise HTTPException(
                status_code=400,
                detail="Document contains no usable text."
            )

        # 3. Split into chunks
        chunks = chunk_text(cleaned_text)

        processed_documents += 1
        total_chunks += len(chunks)

        print(
            f"Tenant={tenant_id}, "
            f"source={document.source}, "
            f"brand={document.brand}, "
            f"chunks={len(chunks)}"
        )

    return IngestResponse(
        tenant_id=tenant_id,
        documents_received=processed_documents,
        message=f"Processed {total_chunks} chunks successfully.",
    )