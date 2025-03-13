import asyncio
import re
from fastapi import FastAPI, HTTPException
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

app = FastAPI()


def normalize_url(url: str) -> str:
    # If the URL doesn't start with "http://" or "https://", prepend "https://"
    if not re.match(r'^https?://', url):
        url = "https://" + url
    return url


@app.get("/crawl")
async def crawl(url: str, query: str = None):
    normalized_url = normalize_url(url)

    # Set up browser configuration
    browser_conf = BrowserConfig(headless=True, verbose=True)

    # Choose a content filter (here, using a fixed threshold filter)
    content_filter = PruningContentFilter(threshold=0.4, threshold_type="fixed")

    # Set up a markdown generator that applies the content filter
    md_generator = DefaultMarkdownGenerator(content_filter=content_filter)

    # Configure the crawler run, bypassing cache to ensure fresh content
    run_conf = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, markdown_generator=md_generator)

    try:
        async with AsyncWebCrawler(config=browser_conf) as crawler:
            result = await crawler.arun(url=normalized_url, config=run_conf)
            return {"markdown": result.markdown.fit_markdown}
    except Exception as e:
        # Return a 400 error with details in case of failure
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=6969)
