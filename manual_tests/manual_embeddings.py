import asyncio

from app.services.retrieval import create_embeddings


async def main():
    chunks = [
        "Asana is a project management platform.",
        "Teams use Asana to manage projects and tasks.",
    ]

    vectors = await create_embeddings(chunks)

    print("Number of vectors:", len(vectors))
    print("Vector dimension:", len(vectors[0]))


asyncio.run(main())