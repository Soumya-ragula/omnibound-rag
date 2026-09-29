import os
import asyncio

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=GEMINI_API_KEY)


async def generate_answer(
    question: str,
    context: str,
    max_retries: int = 3,
) -> str:

    prompt = f"""
You are a helpful RAG assistant.

Answer the user's question using only the provided context.

If the answer is not present in the context, say:
"I don't have enough information in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

    for attempt in range(max_retries):
        try:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                ),
            )

            return response.text.strip()

        except Exception as exc:
            print(
                f"Gemini request failed "
                f"(attempt {attempt + 1}/{max_retries}): {exc}"
            )

            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)

    return (
        "The document was retrieved successfully, "
        "but the AI service is temporarily unavailable. "
        "Please try again shortly."
    )