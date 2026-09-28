from app.vectorstore.pinecone_store import delete_document


delete_document(
    namespace="acme",
    document_id="test-doc#chunk-0",
)

print("Old test document deleted successfully.")