import json
from typing import Dict, Any
from core.abstract_tool import Tool
import requests
from bs4 import BeautifulSoup

class WebSearchTool(Tool):
    def __init__(self):
        super().__init__("web_search", "Perform a web search and return top results")
        self.search_url = "https://www.google.com/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def is_auth_setup(self):
        return True  # No authentication required for this tool

    def execute(self) -> Any:
        parameters = self.get_parameters()
        query = parameters.get('query')
        num_results = parameters.get('num_results', 5)

        try:
            response = requests.get(self.search_url, params={"q": query}, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            search_results = []

            for g in soup.find_all('div', class_='g')[:num_results]:
                anchor = g.find('a')
                if anchor:
                    link = anchor['href']
                    title = g.find('h3', class_='r')
                    title = title.text if title else "No title"
                    snippet = g.find('div', class_='s')
                    snippet = snippet.text if snippet else "No snippet"
                    search_results.append({
                        "title": title,
                        "link": link,
                        "snippet": snippet
                    })

            return json.dumps(search_results)
        except Exception as e:
            return {"error": str(e)}

    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "num_results": {
                    "type": "integer",
                    "description": "The number of search results to return",
                    "default": 5
                }
            },
            "required": ["query"]
        }