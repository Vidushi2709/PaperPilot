import httpx
import xml.etree.ElementTree as ET
from livekit.agents import function_tool

@function_tool
async def search_arxiv(query: str) -> str:
    """Search for AI research papers on Arxiv."""
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "http://export.arxiv.org/api/query",
            params={
                "search_query": f"all:{query}",
                "start": 0,
                "max_results": 3,
                "sortBy": "relevance",
                "sortOrder": "descending",
            },
        )

    root = ET.fromstring(r.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall("atom:entry", ns)

    if not entries:
        return f"No papers found for: {query}"

    results = []
    for entry in entries:
        title = entry.find("atom:title", ns).text.strip()
        summary = entry.find("atom:summary", ns).text.strip()[:300]
        url = entry.find("atom:id", ns).text.strip()
        authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]

        results.append(f"Title: {title}\nAuthors: {', '.join(authors)}\nURL: {url}\nAbstract: {summary}...\n")

    return "\n---\n".join(results)