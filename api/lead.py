from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except Exception:
            data = {}

        lead_entry = {
            "id": f"LEAD_{int(datetime.now().timestamp())}",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "client_name": data.get("client_name", "Ẩn danh"),
            "phone": data.get("phone", "Chưa cung cấp"),
            "email": data.get("email", ""),
            "budget_eur": data.get("budget_eur", 0),
            "monthly_income_eur": data.get("monthly_income_eur", 0),
            "top_match_country": data.get("top_match_country", ""),
            "top_match_program": data.get("top_match_program", ""),
            "match_score": data.get("match_score", 0),
            "notes": data.get("notes", "")
        }

        # Response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {
            "status": "success",
            "message": "Lead received successfully",
            "lead": lead_entry
        }
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "active", "service": "CBlue Leads API"}).encode('utf-8'))
