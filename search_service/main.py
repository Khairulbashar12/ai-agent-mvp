# search_service/main.py

from fastapi import FastAPI, Query
from duckduckgo_search import DDGS

app = FastAPI()

@app.get("/search")
def search_web(query: str = Query(..., description="Search query")):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, region="wt-wt", safesearch="moderate", max_results=5):
            results.append({
                "title": r.get("title"),
                "href": r.get("href"),
                "body": r.get("body")
            })
    return {"query": query, "results": results}
