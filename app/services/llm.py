import os
import asyncio

from dotenv import load_dotenv
from google import genai


load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured")


client = genai.Client(
    api_key=GEMINI_API_KEY,
)

MODEL_NAME = "gemini-3.8-flash"


async def generate_answer(
    question: str,
    context: str,
) -> str:

    prompt = f"""
You are a helpful RAG assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I don't have enough information in the provided documents."

Do not invent information.

Context:
{context}

Question:
{question}

Answer:
"""

    max_retries = 3

    for attempt in range(max_retries):

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )

            if not response.text:
                return "The LLM returned an empty response."

            return response.text.strip()

        except Exception as exc:

            print(
                f"Gemini API attempt "
                f"{attempt + 1}/{max_retries} failed: {exc}"
            )

            if attempt < max_retries - 1:
                await asyncio.sleep(2)

    return (
        "The document was retrieved successfully, "
        "but the AI service is temporarily unavailable. "
        "Please try again shortly."
    )