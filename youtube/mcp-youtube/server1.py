from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx
import json
import os

load_dotenv()

mcp = FastMCP("weather")

API_KEY = os.getenv("SERPER_API_KEY")
SERPER_API_URL = "https://google.serper.dev/search"


async def serch_web(query: str) -> dict | None:
    payload = json.dumps({"q": query, "num": 2})

    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SERPER_API_URL, headers=headers, data=payload, timeout=30.0
            )
            response.raise_for_status()
            results = response.json()
            return results
        except:
            return {"organic": []}


@mcp.tool()
async def get_weather(city: str):
    """
    Get the current weather in a given city

    Args:
        city (str): The city to get the weather for

    Returns:
        The weather information
    """
    results = await serch_web(f"weather in {city}")

    snippets = ""
    for result in results["organic"]:
        snippets += result["snippet"]

    return snippets


if __name__ == "__main__":
    mcp.run(transport="sse")
