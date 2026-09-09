# web_search.py
import os
import asyncio
import aiohttp
from typing import List, Dict

try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS


async def search_duckduckgo(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Asynchronously executes a DuckDuckGo web search.

    Args:
        query (str): The search query string.
        max_results (int): Maximum number of search results to return.

    Returns:
        List[Dict[str, str]]: List of results, each containing 'title', 'href', and 'body'.
    """
    def _run_search():
        try:
            with DDGS() as ddgs:
                raw_results = list(ddgs.text(query, max_results=max_results))
                formatted = []
                for item in raw_results:
                    formatted.append({
                        "title": item.get("title", ""),
                        "href": item.get("href", ""),
                        "body": item.get("body", "")
                    })
                return formatted
        except Exception as e:
            print(f"Error performing DuckDuckGo search for '{query}': {e}")
            return []

    return await asyncio.to_thread(_run_search)


async def read_url_jina(url: str, max_chars: int = 4000, timeout_sec: int = 15) -> str:
    """
    Fetches web page content converted to markdown using Jina Reader (https://r.jina.ai/<url>).

    Args:
        url (str): The target URL to read.
        max_chars (int): Maximum characters to return to avoid context overflow.
        timeout_sec (int): Request timeout in seconds.

    Returns:
        str: Extracted markdown text, or an error message if retrieval fails.
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    jina_url = url if url.startswith("https://r.jina.ai/") else f"https://r.jina.ai/{url}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    jina_api_key = os.getenv("JINA_API_KEY")
    if jina_api_key:
        headers["Authorization"] = f"Bearer {jina_api_key}"

    try:
        timeout = aiohttp.ClientTimeout(total=timeout_sec)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(jina_url, headers=headers) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    if len(text) > max_chars:
                        return text[:max_chars] + f"\n\n[Content truncated to {max_chars} characters...]"
                    return text
                else:
                    return f"(Could not retrieve page content for {url}: HTTP status {resp.status})"
    except asyncio.TimeoutError:
        return f"(Request to read {url} timed out after {timeout_sec} seconds)"
    except Exception as e:
        print(f"Error fetching page via Jina Reader ({url}): {e}")
        return f"(Error reading page {url}: {e})"
