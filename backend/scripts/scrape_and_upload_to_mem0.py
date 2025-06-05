import os
from mem0 import Mem0Client
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawl_site(start_url, allowed_paths=None, max_depth=2):
    visited = set()
    to_visit = [(start_url, 0)]
    results = []

    while to_visit:
        url, depth = to_visit.pop(0)
        if url in visited or depth > max_depth:
            continue
        visited.add(url)
        try:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            results.append({"url": url, "content": soup.get_text()})
            for a in soup.find_all("a", href=True):
                next_url = urljoin(url, a["href"])
                if allowed_paths and not any(next_url.startswith(p) for p in allowed_paths):
                    continue
                if urlparse(next_url).netloc == urlparse(start_url).netloc:
                    to_visit.append((next_url, depth + 1))
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
    return results

def upload_docs_to_mem0(docs, api_key, tags=None):
    client = Mem0Client(api_key=api_key)
    for doc in docs:
        client.add_memory(doc["content"], tags=(tags or []) + [doc["url"]])
        print(f"Uploaded {doc['url']}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--allowed", nargs="*", default=[])
    parser.add_argument("--max_depth", type=int, default=2)
    parser.add_argument("--api_key", default=None)
    args = parser.parse_args()
    docs = crawl_site(args.url, allowed_paths=args.allowed, max_depth=args.max_depth)
    upload_docs_to_mem0(docs, api_key=args.api_key or os.getenv("MEM0_API_KEY"))
