from app.services.retrieval import chunk_text
from app.vectorstore.pinecone_store import upsert_documents


document = """
FastAPI is a modern Python web framework for building APIs.
It supports asynchronous programming and automatic API documentation.
Pydantic is used for data validation and serialization.
RAG stands for Retrieval-Augmented Generation.
RAG systems retrieve relevant information before sending context to an LLM.
"""


chunks = chunk_text(document)

records = []

for i, chunk in enumerate(chunks):
    records.append(
        {
            "id": f"test-doc#chunk-{i}",
            "text": chunk,
        }
    )


upsert_documents(
    namespace="acme",
    records=records,
)

print(f"Successfully inserted {len(records)} chunks.")