from fastapi import APIRouter

from app.schemas import QueryRequest, QueryResponse
from app.services.retrieval import answer_question


router = APIRouter()


@router.post(
    "/tenants/{tenant_id}/query",
    response_model=QueryResponse,
)
async def query(
    tenant_id: str,
    request: QueryRequest,
):
    result = await answer_question(
        question=request.question,
        namespace=tenant_id,
    )

    return QueryResponse(
        answer=result["answer"],
        sources=result["sources"],
    )