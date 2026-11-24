from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Add parent directory to path to import matching_engine
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from matching_engine import evaluate_client_profile

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            profile = json.loads(post_data.decode('utf-8'))
        except Exception:
            profile = {}

        # Load master programs
        master_file = os.path.join(parent_dir, "data", "eu_immigration_master.json")
        try:
            with open(master_file, "r", encoding="utf-8") as f:
                master = json.load(f)
                all_programs = master.get("all_programs", [])
        except Exception:
            all_programs = []

        results = evaluate_client_profile(profile, all_programs)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        response = {
            "status": "success",
            "total_matches": len(results),
            "top_matches": results[:5]
        }
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
