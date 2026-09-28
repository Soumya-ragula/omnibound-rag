import httpx
from bs4 import BeautifulSoup


async def extract_text_from_url(url: str) -> str:
    async with httpx.AsyncClient(
        timeout=20.0,
        follow_redirects=True
    ) as client:
        response = await client.get(url)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove elements that usually don't contain useful article content
    for element in soup(
        ["script", "style", "noscript", "header", "footer", "nav"]
    ):
        element.decompose()

    text = soup.get_text(separator=" ", strip=True)

    return text


def clean_text(text: str) -> str:
    return " ".join(text.split())