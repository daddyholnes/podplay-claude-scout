"""
Utility API routes for extracting site links for Mem0 ingestion UI
"""
from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

bp = Blueprint('utils', __name__)

@bp.route('/api/utils/extract_links', methods=['POST'])
def extract_links():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'links': []})
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        links = set()
        for a in soup.find_all('a', href=True):
            link = urljoin(url, a['href'])
            # Only include links within the same domain
            if urlparse(link).netloc == urlparse(url).netloc:
                # Only top-level subdirs
                parts = urlparse(link).path.split('/')
                if len(parts) > 1 and parts[1]:
                    links.add(f"{urlparse(link).scheme}://{urlparse(link).netloc}/{parts[1]}")
        return jsonify({'links': sorted(list(links))})
    except Exception as e:
        return jsonify({'links': [], 'error': str(e)})
