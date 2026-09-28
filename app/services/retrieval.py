from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.vectorstore.pinecone_store import index
from app.services.llm import generate_answer


def chunk_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
    )

    return splitter.split_text(text)


def retrieve_context(
    question: str,
    namespace: str,
    top_k: int = 3,
):
    results = index.search(
        namespace=namespace,
        query={
            "inputs": {
                "text": question,
            },
            "top_k": top_k,
        },
    )

    contexts = []
    sources = []

    for hit in results.result.hits:
        text = hit.fields.get("text")

        if text:
            contexts.append(text)

            sources.append(
                {
                    "id": hit.id,
                    "filename": hit.fields.get("filename"),
                    "chunk_index": hit.fields.get("chunk_index"),
                    "score": hit.score,
                }
            )

    return "\n\n".join(contexts), sources


async def answer_question(
    question: str,
    namespace: str,
):
    context, sources = retrieve_context(
        question=question,
        namespace=namespace,
    )

    if not context:
        return {
            "answer": "I don't have enough information in the provided documents.",
            "sources": [],
        }

    answer = await generate_answer(
        question=question,
        context=context,
    )

    return {
        "answer": answer,
        "sources": sources,
    }