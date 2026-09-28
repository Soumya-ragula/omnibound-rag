from app.vectorstore.pinecone_store import index


query = "What is FastAPI?"

results = index.search(
    namespace="acme",
    query={
        "inputs": {
            "text": query
        },
        "top_k": 3,
    },
)

print(results)