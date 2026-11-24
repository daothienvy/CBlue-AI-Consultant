"""
leads_manager.py
Manages lead collection, persistence, and export for CBlue Immigration consultants.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any

LEADS_FILE = "data/leads.json"

def init_leads_store():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def save_lead(client_profile: Dict[str, Any], top_match: Dict[str, Any]) -> bool:
    """Saves a new lead record with contact info, profile, and top matched program."""
    init_leads_store()
    try:
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            leads = json.load(f)
    except Exception:
        leads = []

    lead_entry = {
        "id": f"LEAD_{int(datetime.now().timestamp())}",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "client_name": client_profile.get("client_name", "Ẩn danh"),
        "phone": client_profile.get("phone", "Chưa cung cấp"),
        "email": client_profile.get("email", ""),
        "budget_eur": client_profile.get("budget_eur", 0),
        "monthly_income_eur": client_profile.get("monthly_income_eur", 0),
        "physical_stay": client_profile.get("physical_stay_capability", ""),
        "primary_goal": client_profile.get("primary_goal", ""),
        "family_composition": client_profile.get("family_composition", ""),
        "education": client_profile.get("education_level", ""),
        "top_match_country": top_match.get("country_vi", ""),
        "top_match_program": top_match.get("program_name", ""),
        "match_score": top_match.get("match_score", 0),
        "notes": client_profile.get("notes", "")
    }

    leads.insert(0, lead_entry)

    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)

    return True

def get_all_leads() -> List[Dict[str, Any]]:
    """Retrieves all leads as a list of dicts."""
    init_leads_store()
    try:
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []
