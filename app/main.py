from fastapi import FastAPI

from app.routers.query import router as query_router
from app.routers.ingest import router as ingest_router


app = FastAPI(
    title="Omnibound RAG API",
)


@app.get("/")
async def root():
    return {
        "message": "Omnibound RAG API is running"
    }


app.include_router(query_router)
app.include_router(ingest_router)