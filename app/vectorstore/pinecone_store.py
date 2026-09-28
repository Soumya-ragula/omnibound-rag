import os

from dotenv import load_dotenv
from pinecone import Pinecone


load_dotenv(override=True)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

PINECONE_INDEX = os.getenv(
    "PINECONE_INDEX",
    "omnibound-rag",
)

pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index(PINECONE_INDEX)


def upsert_documents(
    namespace: str,
    records: list[dict],
):
    index.upsert_records(
        namespace=namespace,
        records=records,
    )


def delete_document(
    namespace: str,
    document_id: str,
):
    index.delete(
        ids=[document_id],
        namespace=namespace,
    )