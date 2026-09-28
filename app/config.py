
import os

from dotenv import load_dotenv


load_dotenv(override=True)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "omnibound-rag")

EMBEDDING_MODEL = "text-embedding-3-small"