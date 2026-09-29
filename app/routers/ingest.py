from fastapi import APIRouter, File, UploadFile, HTTPException

from app.services.retrieval import chunk_text
from app.services.document_loader import extract_text_from_pdf
from app.vectorstore.pinecone_store import upsert_documents


router = APIRouter()


@router.post("/tenants/{tenant_id}/ingest")
async def ingest_document(
    tenant_id: str,
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is required",
        )

    content = await file.read()

    filename = file.filename.lower()

    # Extract text from TXT or PDF
    if filename.endswith(".txt"):
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="TXT file must use UTF-8 encoding",
            )

    elif filename.endswith(".pdf"):
        text = extract_text_from_pdf(content)

    else:
        raise HTTPException(
            status_code=400,
            detail="Only TXT and PDF files are supported",
        )

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text found in the document",
        )

    # Split document into chunks
    chunks = chunk_text(text)

    # Create Pinecone records
    records = []

    for i, chunk in enumerate(chunks):
        records.append(
            {
                "id": f"{file.filename}#chunk-{i}",
                "text": chunk,
                "filename": file.filename,
                "chunk_index": i,
            }
        )

    # Store records in the tenant's namespace
    upsert_documents(
        namespace=tenant_id,
        records=records,
    )

    return {
        "message": "Document ingested successfully",
        "tenant_id": tenant_id,
        "filename": file.filename,
        "chunks": len(chunks),
    }
