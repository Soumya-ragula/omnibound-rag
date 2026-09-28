from app.vectorstore.pinecone_store import index


stats = index.describe_index_stats()

print("Pinecone connection successful!")
print(stats)