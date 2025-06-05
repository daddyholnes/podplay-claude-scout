"""
Ingestion API routes for Mem0-powered knowledge ingestion (file upload & web scraping)
Accessible to Mama Bear agents and user UI triggers.
"""

import os
import subprocess
from flask import Blueprint, request, jsonify

bp = Blueprint('ingestion', __name__)

UPLOAD_SCRIPT = os.path.join(os.path.dirname(__file__), '../scripts/upload_to_mem0.py')
SCRAPE_SCRIPT = os.path.join(os.path.dirname(__file__), '../scripts/scrape_and_upload_to_mem0.py')

@bp.route('/api/ingest/upload', methods=['POST'])
def upload_to_mem0():
    data = request.json
    filepath = data.get('filepath')
    tags = data.get('tags', [])
    api_key = data.get('api_key', os.environ.get('MEM0_API_KEY'))
    if not filepath or not os.path.exists(filepath):
        return jsonify({'success': False, 'error': 'File not found'}), 400
    cmd = ['python', UPLOAD_SCRIPT, filepath]
    if tags:
        cmd += ['--tags'] + tags
    if api_key:
        cmd += ['--api_key', api_key]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return jsonify({'success': proc.returncode == 0, 'stdout': proc.stdout, 'stderr': proc.stderr})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/ingest/scrape', methods=['POST'])
def scrape_and_upload():
    data = request.json
    url = data.get('url')
    allowed = data.get('allowed', [])
    max_depth = str(data.get('max_depth', 2))
    api_key = data.get('api_key', os.environ.get('MEM0_API_KEY'))
    if not url:
        return jsonify({'success': False, 'error': 'URL required'}), 400
    cmd = ['python', SCRAPE_SCRIPT, url]
    if allowed:
        cmd += ['--allowed'] + allowed
    cmd += ['--max_depth', max_depth]
    if api_key:
        cmd += ['--api_key', api_key]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        return jsonify({'success': proc.returncode == 0, 'stdout': proc.stdout, 'stderr': proc.stderr})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
