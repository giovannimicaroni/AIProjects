import requests
from langchain.tools import BaseTool
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class SearchPapersTool(BaseTool):
    name: str = "search_papers"
    description: str = (
        "Search for academic papers using a natural language query. "
        "Returns a list of papers with titles, authors, IDs, and abstracts."
    )

    def _run(self, query: str):
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": 10,
            "fields": "title,authors,year,abstract,url"
        }
        # Use a requests Session with retries to handle transient 429/5xx responses
        session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))

        try:
            r = session.get(url, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
            return data.get("data", [])
        except requests.exceptions.HTTPError as e:
            status = None
            if hasattr(e, "response") and e.response is not None:
                status = e.response.status_code
            logging.warning("SearchPapersTool HTTP error: %s (status=%s)", e, status)
            if status == 429:
                return "Error: rate limited by Semantic Scholar API (429). Try again later or add an API key."
            return f"HTTP error while searching papers: {e}"
        except Exception as e:
            logging.exception("SearchPapersTool request failed")
            return f"Request failed: {e}"
    
    async def _arun(self, query: str):

        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": 10,
            "fields": "title,authors,year,abstract,url"
        }

        # Async retry loop with exponential backoff for 429/5xx
        async with aiohttp.ClientSession() as session:
            for attempt in range(5):
                async with session.get(url, params=params) as resp:
                    if resp.status == 429:
                        wait = 2 ** attempt
                        logging.warning("SearchPapersTool rate limited (429). Backing off %s seconds (attempt %s)", wait, attempt + 1)
                        await asyncio.sleep(wait)
                        continue
                    if resp.status >= 400:
                        text = await resp.text()
                        return f"HTTP error {resp.status}: {text}"
                    data = await resp.json()
                    return data.get("data", [])

        return "Error: failed to retrieve papers after retries"

class GetPaperMetadataTool(BaseTool):
    name: str = "get_paper_metadata"
    description: str = (
        "Retrieve metadata for a paper using its Semantic Scholar ID, DOI, or arXiv ID. "
        "Returns title, authors, abstract, year, venue, reference count, citation count, etc."
    )

    def _run(self, paper_id: str):
        url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
        params = {
            "fields": "title,authors,abstract,year,venue,url,"
                      "referenceCount,citationCount,fieldsOfStudy"
        }

        session = requests.Session()
        retries = Retry(
            total=4,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))

        try:
            response = session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            status = None
            if hasattr(e, "response") and e.response is not None:
                status = e.response.status_code
            logging.warning("GetPaperMetadataTool HTTP error: %s (status=%s)", e, status)
            if status == 429:
                return {"error": "rate limited by Semantic Scholar API (429)"}
            return {"error": str(e)}
        except Exception as e:
            logging.exception("GetPaperMetadataTool request failed")
            return {"error": str(e)}
    
    async def _arun(self, paper_id: str):

        url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
        params = {
            "fields": "title,authors,abstract,year,venue,url,"
                      "referenceCount,citationCount,fieldsOfStudy"
        }

        async with aiohttp.ClientSession() as session:
            for attempt in range(4):
                async with session.get(url, params=params) as resp:
                    if resp.status == 429:
                        wait = 2 ** attempt
                        logging.warning("GetPaperMetadataTool rate limited (429). Backing off %s seconds (attempt %s)", wait, attempt + 1)
                        await asyncio.sleep(wait)
                        continue
                    if resp.status >= 400:
                        text = await resp.text()
                        return {"error": f"HTTP error {resp.status}: {text}"}
                    return await resp.json()

        return {"error": "failed to retrieve metadata after retries"}


class FindPDFLinkTool(BaseTool):
    name: str = "find_pdf_link"
    description: str = (
        "Given a Semantic Scholar paper ID or URL, scrape the page and return a direct PDF link if available."
    )

    def _find_link(self, response):
        # Accept either a requests/response-like object with `.text` or a raw HTML string
        html = response.text if hasattr(response, "text") else response
        soup = BeautifulSoup(html, "html.parser")

        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.lower().endswith(".pdf"):
                if href.startswith("/"):
                    return "https://www.semanticscholar.org" + href

                return href

        return None


    def _run(self, paper_id_or_url: str):
        if paper_id_or_url.startswith('http'):
            url = paper_id_or_url
        else:
            url = f'https://www.semanticscholar.org/paper/{paper_id_or_url}'
        

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return self._find_link(response)
        except requests.exceptions.HTTPError as e:
            status = None
            if hasattr(e, "response") and e.response is not None:
                status = e.response.status_code
            logging.warning("FindPDFLinkTool HTTP error: %s (status=%s)", e, status)
            return None
        except Exception as e:
            logging.exception("FindPDFLinkTool request failed")
            return None

    async def _arun(self, paper_id_or_url: str):
        if paper_id_or_url.startswith("http"):
            url = paper_id_or_url
        else:
            url = f"https://www.semanticscholar.org/paper/{paper_id_or_url}"

        async with aiohttp.ClientSession() as session:
            for attempt in range(4):
                async with session.get(url) as resp:
                    if resp.status == 429:
                        wait = 2 ** attempt
                        logging.warning("FindPDFLinkTool rate limited (429). Backing off %s seconds (attempt %s)", wait, attempt + 1)
                        await asyncio.sleep(wait)
                        continue
                    if resp.status >= 400:
                        return None
                    text = await resp.text()
                    return self._find_link(text)

        return None