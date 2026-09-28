from fastapi import APIRouter, File, UploadFile, HTTPException

from app.services.retrieval import chunk_text
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

    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="Only TXT files are supported currently",
        )

    content = await file.read()

    text = content.decode("utf-8")

    chunks = chunk_text(text)

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