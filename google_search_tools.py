from smolagents import Tool
from googleapiclient.discovery import build
import os

class GoogleSearchTool(Tool):
    name = "web_search"
    description = """Performs a google web search for a query then returns top search results in markdown format."""

    inputs = {
        "query": {
            "type": "string",
            "description": "The query to perform a web search for"
        }
    }
    output_type = "string"

    skip_forward_signature_validation = True

    def __init__(
        self,
        api_key: str | None = None,
        search_engine_id: str | None = None,
        num_results: int = 10,
        **kwargs,
    ):
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set")
        if not search_engine_id:
            raise ValueError("GOOGLE_SEARCH_ENGINE_ID is not set")

        self.cse = build(
            "customsearch",
            "v1",
            developerKey=api_key
        ).cse()
        self.cx = search_engine_id
        self.num = num_results
        super().__init__(**kwargs)

    def _collect_params(self) -> dict:
        return {}
    
    def forward(self, query: str, *args, **kwargs) -> str:
        params = {
            "q": query,
            "cx": self.cx,
            "fields": "items(link, title, snippet)",
            "num": self.num,
        }
        
        params = params | self._collect_params(*args, **kwargs)
        res = self.cse.list(**params).execute()
        if "items" not in res:
            return "No results found"
        
        return "\n\n".join(f"{item['title']}\n{item['link']}\n{item['snippet']}" for item in res["items"])

class GoogleSiteSearchTool(GoogleSearchTool):
    name = "site_search"
    description = """Searches a specific website for a given query and returns the site contents in markdown format. Use when information is likely to be found on a particular domain, such as reddit.com, wikipedia.org, ieee.org, or arxiv.org."""
    inputs = {
        "query": {
            "type": "string",
            "description": "The query to perform search."
        },
        "site": {
            "type": "string",
            "description": "The domain of the site on which to search",
        },
    }

    def _collect_params(self, site: str) -> dict:
        return {
            "siteSearch": site,
            "siteSearchFilter": "i",
        }