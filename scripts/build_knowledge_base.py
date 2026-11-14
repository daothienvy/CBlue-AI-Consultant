#!/usr/bin/env python3
"""
build_knowledge_base.py
Extracts data from eu_schengen_immigration_analysis.xlsx, enriches it with the 5-tier
standardized checklist framework, and writes:
1. data/countries/{country_slug}.json
2. data/countries/{country_slug}.md
3. data/eu_immigration_master.json
4. data/archetypes_checklists.json
"""

import os
import re
import json
import openpyxl
from collections import defaultdict
from standard_schemas import ARCHETYPES, get_archetype_for_program

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[-\s]+', '_', text)

EXCEL_PATH = 'eu_schengen_immigration_analysis.xlsx'
DATA_DIR = 'data'
COUNTRIES_DIR = os.path.join(DATA_DIR, 'countries')
os.makedirs(COUNTRIES_DIR, exist_ok=True)

wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)

# 1. Parse 'Tổng Quan 30 Quốc Gia'
sheet_ov = wb['Tổng Quan 30 Quốc Gia']
countries_overview = {}
for r in range(5, sheet_ov.max_row + 1):
    c_en = sheet_ov.cell(r, 2).value
    if not c_en:
        continue
    c_en = str(c_en).strip()
    c_slug = slugify(c_en)
    c_vi = str(sheet_ov.cell(r, 3).value or '').strip()
    eu_status = str(sheet_ov.cell(r, 4).value or '').strip()
    portal = str(sheet_ov.cell(r, 5).value or '').strip()
    num_progs = sheet_ov.cell(r, 6).value
    mipex = sheet_ov.cell(r, 7).value
    refusal = sheet_ov.cell(r, 8).value
    gv_status = str(sheet_ov.cell(r, 9).value or '').strip()
    dn_status = str(sheet_ov.cell(r, 10).value or '').strip()
    difficulty = str(sheet_ov.cell(r, 11).value or '').strip()
    
    countries_overview[c_en] = {
        "country_en": c_en,
        "country_vi": c_vi,
        "slug": c_slug,
        "eu_schengen_status": eu_status,
        "official_portal": portal,
        "num_programs": num_progs,
        "mipex_score": mipex,
        "visa_refusal_rate": refusal,
        "golden_visa_status": gv_status,
        "digital_nomad_status": dn_status,
        "difficulty_rating": difficulty
    }

# 2. Parse 'Chỉ Số Khó - Dễ'
difficulty_stats = {}
if 'Chỉ Số Khó - Dễ' in wb.sheetnames:
    s_diff = wb['Chỉ Số Khó - Dễ']
    for r in range(6, s_diff.max_row + 1):
        c_en = s_diff.cell(r, 2).value
        if c_en:
            c_en = str(c_en).strip()
            difficulty_stats[c_en] = {
                "rank": s_diff.cell(r, 1).value,
                "permits_per_1000": s_diff.cell(r, 5).value,
                "processing_months": s_diff.cell(r, 6).value,
                "years_to_pr": s_diff.cell(r, 7).value,
                "years_to_citizenship": s_diff.cell(r, 8).value,
                "difficulty_level": s_diff.cell(r, 10).value,
                "composite_score": s_diff.cell(r, 11).value,
                "notes": str(s_diff.cell(r, 12).value or '').strip()
            }

# 3. Parse 'Thay Đổi CS 2025-2026'
policy_changes = defaultdict(list)
if 'Thay Đổi CS 2025-2026' in wb.sheetnames:
    s_ch = wb['Thay Đổi CS 2025-2026']
    for r in range(5, s_ch.max_row + 1):
        time_period = str(s_ch.cell(r, 2).value or '').strip()
        country_area = str(s_ch.cell(r, 3).value or '').strip()
        change = str(s_ch.cell(r, 4).value or '').strip()
        impact = str(s_ch.cell(r, 5).value or '').strip()
        status = str(s_ch.cell(r, 6).value or '').strip()
        detail = str(s_ch.cell(r, 7).value or '').strip()
        if country_area and change:
            item = {
                "time": time_period,
                "region": country_area,
                "change": change,
                "impact": impact,
                "status": status,
                "detail": detail
            }
            policy_changes[country_area].append(item)

# 4. Parse 'Nguồn Tham Khảo'
references = defaultdict(list)
if 'Nguồn Tham Khảo' in wb.sheetnames:
    s_ref = wb['Nguồn Tham Khảo']
    for r in range(5, s_ref.max_row + 1):
        cat = str(s_ref.cell(r, 2).value or '').strip()
        source_name = str(s_ref.cell(r, 3).value or '').strip()
        url = str(s_ref.cell(r, 4).value or '').strip()
        desc = str(s_ref.cell(r, 5).value or '').strip()
        target_country = str(s_ref.cell(r, 6).value or '').strip()
        if target_country and source_name:
            references[target_country].append({
                "category": cat,
                "name": source_name,
                "url": url,
                "description": desc
            })

# 5. Parse 'EU Blue Card' salary thresholds
blue_card_info = {}
if 'EU Blue Card' in wb.sheetnames:
    s_bc = wb['EU Blue Card']
    for r in range(5, s_bc.max_row + 1):
        c_en = s_bc.cell(r, 2).value
        if c_en:
            c_en = str(c_en).strip()
            threshold = s_bc.cell(r, 3).value
            shortage = s_bc.cell(r, 4).value
            pr_time = s_bc.cell(r, 5).value
            note = str(s_bc.cell(r, 6).value or '').strip()
            participating = str(s_bc.cell(r, 8).value or '').strip()
            blue_card_info[c_en] = {
                "threshold_eur_per_year": threshold,
                "shortage_occupation_threshold": shortage,
                "pr_time": pr_time,
                "note": note,
                "participating": participating
            }

# 6. Parse 'Golden Visa & Đầu Tư'
golden_visa_info = defaultdict(list)
if 'Golden Visa & Đầu Tư' in wb.sheetnames:
    s_gv = wb['Golden Visa & Đầu Tư']
    for r in range(5, s_gv.max_row + 1):
        c_en = s_gv.cell(r, 2).value
        if c_en:
            c_en = str(c_en).strip()
            p_name = str(s_gv.cell(r, 3).value or '').strip()
            status = str(s_gv.cell(r, 4).value or '').strip()
            min_inv = str(s_gv.cell(r, 5).value or '').strip()
            inv_type = str(s_gv.cell(r, 6).value or '').strip()
            pr_time = str(s_gv.cell(r, 7).value or '').strip()
            cit_time = str(s_gv.cell(r, 8).value or '').strip()
            changes = str(s_gv.cell(r, 9).value or '').strip()
            notes = str(s_gv.cell(r, 10).value or '').strip()
            golden_visa_info[c_en].append({
                "program_name": p_name,
                "status": status,
                "min_investment": min_inv,
                "investment_type": inv_type,
                "pr_timeline": pr_time,
                "citizenship_timeline": cit_time,
                "changes_2025_2026": changes,
                "notes": notes
            })

# 7. Parse 'Digital Nomad Visa'
digital_nomad_info = {}
if 'Digital Nomad Visa' in wb.sheetnames:
    s_dn = wb['Digital Nomad Visa']
    for r in range(5, s_dn.max_row + 1):
        c_en = s_dn.cell(r, 2).value
        if c_en:
            c_en = str(c_en).strip()
            min_income = s_dn.cell(r, 3).value
            validity = str(s_dn.cell(r, 4).value or '').strip()
            tax = str(s_dn.cell(r, 5).value or '').strip()
            leads_to_pr = str(s_dn.cell(r, 6).value or '').strip()
            family = str(s_dn.cell(r, 7).value or '').strip()
            conds = str(s_dn.cell(r, 8).value or '').strip()
            digital_nomad_info[c_en] = {
                "min_monthly_income_eur": min_income,
                "validity": validity,
                "tax_regime": tax,
                "leads_to_pr": leads_to_pr,
                "family_allowed": family,
                "conditions": conds
            }

# 8. Parse 'Thu Nhập Thụ Động - FIP'
fip_info = {}
if 'Thu Nhập Thụ Động - FIP' in wb.sheetnames:
    s_fip = wb['Thu Nhập Thụ Động - FIP']
    for r in range(5, s_fip.max_row + 1):
        c_en = s_fip.cell(r, 2).value
        if c_en:
            c_en = str(c_en).strip()
            p_name = str(s_fip.cell(r, 3).value or '').strip()
            min_inc = s_fip.cell(r, 4).value
            savings = str(s_fip.cell(r, 5).value or '').strip()
            work_allowed = str(s_fip.cell(r, 6).value or '').strip()
            pr_time = str(s_fip.cell(r, 7).value or '').strip()
            cit_time = str(s_fip.cell(r, 8).value or '').strip()
            conds = str(s_fip.cell(r, 9).value or '').strip()
            fip_info[c_en] = {
                "program_name": p_name,
                "min_monthly_income_eur": min_inc,
                "savings_required": savings,
                "work_allowed": work_allowed,
                "pr_timeline": pr_time,
                "citizenship_timeline": cit_time,
                "conditions": conds
            }

# 9. Parse 'Startup & Doanh Nhân'
startup_info = {}
if 'Startup & Doanh Nhân' in wb.sheetnames:
    s_st = wb['Startup & Doanh Nhân']
    for r in range(5, s_st.max_row + 1):
        c_en = s_st.cell(r, 2).value
        if c_en:
            c_en = str(c_en).strip()
            p_name = str(s_st.cell(r, 3).value or '').strip()
            capital = str(s_st.cell(r, 4).value or '').strip()
            living_costs = str(s_st.cell(r, 5).value or '').strip()
            authority = str(s_st.cell(r, 6).value or '').strip()
            validity = str(s_st.cell(r, 7).value or '').strip()
            pr_time = str(s_st.cell(r, 8).value or '').strip()
            conds = str(s_st.cell(r, 9).value or '').strip()
            startup_info[c_en] = {
                "program_name": p_name,
                "capital_required": capital,
                "living_costs": living_costs,
                "approval_authority": authority,
                "validity": validity,
                "pr_timeline": pr_time,
                "conditions": conds
            }

# 10. Parse 'Chi Tiết Diện Định Cư' (The core list of programs)
sheet_dt = wb['Chi Tiết Diện Định Cư']
country_programs_raw = defaultdict(list)

for r in range(5, sheet_dt.max_row + 1):
    c_en = sheet_dt.cell(r, 2).value
    p_name = sheet_dt.cell(r, 3).value
    if not c_en or not p_name or str(c_en).strip().startswith('■'):
        continue
    c_en = str(c_en).strip()
    p_name = str(p_name).strip()
    category = str(sheet_dt.cell(r, 4).value or '').strip()
    financial = str(sheet_dt.cell(r, 5).value or '').strip()
    processing = str(sheet_dt.cell(r, 6).value or '').strip()
    pr_time = str(sheet_dt.cell(r, 7).value or '').strip()
    cit_time = str(sheet_dt.cell(r, 8).value or '').strip()
    language = str(sheet_dt.cell(r, 9).value or '').strip()
    conditions = str(sheet_dt.cell(r, 10).value or '').strip()

    country_programs_raw[c_en].append({
        "program_name": p_name,
        "category": category,
        "financial_requirement": financial,
        "processing_time": processing,
        "timeline_pr": pr_time,
        "timeline_citizenship": cit_time,
        "language_requirement": language,
        "conditions": conditions
    })

# Helpers to extract numeric values for matching
def extract_investment_eur(fin_str, category_str, p_name):
    fin = fin_str.lower()
    # Check for K or M
    m_val = re.search(r'€?(\d+[\.,]?\d*)\s*(triệu|m|tr)', fin)
    if m_val:
        return float(m_val.group(1).replace(',', '.')) * 1000000
    k_val = re.search(r'€?(\d+[\.,]?\d*)\s*(k|nghìn)', fin)
    if k_val:
        return float(k_val.group(1).replace(',', '.')) * 1000
    num_val = re.search(r'€\s*(\d{1,3}(?:[,\.]\d{3})+)', fin_str)
    if num_val:
        num = num_val.group(1).replace('.', '').replace(',', '')
        return float(num)
    digits = re.findall(r'(\d+)', fin_str.replace('.', '').replace(',', ''))
    if digits:
        val = int(digits[0])
        if val >= 20000:
            return float(val)
    if "golden visa" in p_name.lower():
        if "portugal" in p_name.lower():
            return 500000.0
        if "greece" in p_name.lower():
            return 250000.0
        if "spain" in p_name.lower():
            return 500000.0
        if "malta" in p_name.lower():
            return 150000.0
        if "hungary" in p_name.lower():
            return 250000.0
        return 250000.0
    return 0.0

def extract_monthly_income_eur(fin_str, category_str, p_name, country_en):
    fin = fin_str.lower()
    # If nomad or FIP
    if "tháng" in fin or "month" in fin or "digital nomad" in p_name.lower() or "fip" in p_name.lower() or "d7" in p_name.lower() or "d8" in p_name.lower() or "visiteur" in p_name.lower() or "non-lucrative" in p_name.lower():
        # Check specific table first
        if country_en in digital_nomad_info and "digital nomad" in p_name.lower():
            dn_val = digital_nomad_info[country_en].get("min_monthly_income_eur")
            if dn_val and isinstance(dn_val, (int, float)):
                return float(dn_val)
        if country_en in fip_info and ("fip" in p_name.lower() or "thụ động" in p_name.lower() or "d7" in p_name.lower() or "visiteur" in p_name.lower()):
            fip_val = fip_info[country_en].get("min_monthly_income_eur")
            if fip_val and isinstance(fip_val, (int, float)):
                return float(fip_val)
        # Parse from string
        nums = re.findall(r'€\s*(\d+[\.,]?\d*)', fin_str)
        if nums:
            v = float(nums[0].replace(',', '.'))
            if v < 15000:
                return v
    return 0.0

def determine_physical_stay(archetype_id, country_en, p_name):
    if archetype_id == "golden_visa":
        if "portugal" in country_en.lower():
            return 7
        if "malta" in country_en.lower():
            return 0
        if "greece" in country_en.lower():
            return 0
        if "hungary" in country_en.lower():
            return 0
        if "cyprus" in country_en.lower():
            return 1 # 1 day every 2 years
        return 7
    elif archetype_id in ["blue_card", "passive_income", "startup_entrepreneur"]:
        return 183
    elif archetype_id == "digital_nomad":
        return 183
    return 183

# Build enriched country dossiers
all_enriched_countries = {}
master_programs_list = []

for c_en, c_meta in countries_overview.items():
    c_slug = c_meta["slug"]
    c_diff = difficulty_stats.get(c_en, {})
    c_changes = policy_changes.get(c_en, []) + policy_changes.get("EU", [])
    c_refs = references.get(c_en, [])
    
    # Process programs for this country
    raw_progs = country_programs_raw.get(c_en, [])
    enriched_progs = []
    
    for idx, p in enumerate(raw_progs, 1):
        p_name = p["program_name"]
        cat_str = p["category"]
        arch_id = get_archetype_for_program(cat_str, p_name)
        arch_schema = ARCHETYPES[arch_id]
        
        inv_eur = extract_investment_eur(p["financial_requirement"], cat_str, p_name)
        inc_eur = extract_monthly_income_eur(p["financial_requirement"], cat_str, p_name, c_en)
        stay_days = determine_physical_stay(arch_id, c_en, p_name)
        
        # Check specific cross-sheet data
        bc_data = blue_card_info.get(c_en) if arch_id == "blue_card" else None
        dn_data = digital_nomad_info.get(c_en) if arch_id == "digital_nomad" else None
        fip_data = fip_info.get(c_en) if arch_id == "passive_income" else None
        st_data = startup_info.get(c_en) if arch_id == "startup_entrepreneur" else None
        
        # Parse years to PR and citizenship as numbers
        pr_match = re.search(r'(\d+)', str(p["timeline_pr"]))
        pr_years = int(pr_match.group(1)) if pr_match else 5
        cit_match = re.search(r'(\d+)', str(p["timeline_citizenship"]))
        cit_years = int(cit_match.group(1)) if cit_match else 10
        
        # Build 5-tier checklist tailored for this country and program
        custom_checklist = {
            "tier1_civil_identity": [dict(x) for x in arch_schema["checklist"]["tier1_civil_identity"]],
            "tier2_financial_funds": [dict(x) for x in arch_schema["checklist"]["tier2_financial_funds"]],
            "tier3_specialized_investment": [dict(x) for x in arch_schema["checklist"]["tier3_specialized_investment"]],
            "tier4_accommodation_health": [dict(x) for x in arch_schema["checklist"]["tier4_accommodation_health"]],
            "tier5_legalization_submission": [dict(x) for x in arch_schema["checklist"]["tier5_legalization_submission"]]
        }
        
        # Tailor checklist based on country and specific program
        if arch_id == "golden_visa":
            if "portugal" in c_en.lower():
                custom_checklist["tier3_specialized_investment"].append({
                    "item": "Chứng chỉ mua Quỹ đầu tư mạo hiểm (CMVM Regulated Fund) €500,000",
                    "detail": "Bồ Đào Nha đã kết thúc diện BĐS từ 10/2023. Diện phổ biến hiện nay là đầu tư tối thiểu €500,000 vào Quỹ đầu tư tư nhân/mạo hiểm (VC Fund) có giám sát của Ủy ban Chứng khoán CMVM."
                })
                custom_checklist["tier5_legalization_submission"].append({
                    "item": "Lợi thế Luật Quốc tịch Bồ Đào Nha 2024-2026",
                    "detail": "Thời gian 5 năm để xin nhập quốc tịch bắt đầu tính từ ngày nộp hồ sơ xin thẻ cư trú lần đầu (thay vì tính từ ngày được cấp thẻ như trước)."
                })
            elif "greece" in c_en.lower():
                custom_checklist["tier3_specialized_investment"].append({
                    "item": "Hợp đồng mua BĐS theo phân vùng mới 2024-2026 (€250K / €400K / €800K)",
                    "detail": "Vùng Tier 1 (€800K): Athens, Thessaloniki, Mykonos, Santorini và các đảo lớn; Vùng Tier 2 (€400K): Các khu vực còn lại; Vùng Tier 3 (€250K): BĐS chuyển đổi từ thương mại sang để ở hoặc công trình di sản phục dựng."
                })
            elif "hungary" in c_en.lower():
                custom_checklist["tier3_specialized_investment"].append({
                    "item": "Chứng chỉ Quỹ BĐS Khách Đầu Tư (Guest Investor Fund) €250,000",
                    "detail": "Chương trình Golden Visa mới của Hungary (GIP 2024-2026): Cấp thẻ cư trú có thời hạn lên tới 10 năm ngay từ đầu cho cả gia đình thông qua đầu tư tối thiểu €250,000 vào chứng chỉ quỹ BĐS được chỉ định."
                })
            elif "malta" in c_en.lower():
                custom_checklist["tier3_specialized_investment"].append({
                    "item": "Hồ sơ thường trú nhân Malta MPRP (Malta Permanent Residence Programme)",
                    "detail": "Yêu cầu: Thuê nhà tối thiểu €10,000-€12,000/năm (hoặc mua BĐS €300,000-€350,000) + Đóng góp chính phủ €28,000-€58,000 + Quyên góp từ thiện €2,000 + Chứng minh tài sản ròng tối thiểu €500,000 (trong đó có €150,000 tài sản thanh khoản)."
                })
                
        elif arch_id == "blue_card":
            if bc_data and bc_data.get("threshold_eur_per_year"):
                custom_checklist["tier2_financial_funds"][0]["detail"] += f" (Ngưỡng lương quy định tại {c_en}: €{bc_data['threshold_eur_per_year']:,}/năm; ngành thiếu hụt: {bc_data.get('shortage_occupation_threshold')})."
            if "germany" in c_en.lower():
                custom_checklist["tier5_legalization_submission"].append({
                    "item": "Rút ngắn thời gian lấy Thường trú nhân (PR) Đức",
                    "detail": "Được cấp Thường trú nhân (Niederlassungserlaubnis) chỉ sau 21 tháng nếu có tiếng Đức trình độ B1; hoặc sau 27 tháng nếu có tiếng Đức A1."
                })
                
        elif arch_id == "digital_nomad":
            if dn_data:
                inc_req = dn_data.get("min_monthly_income_eur")
                if inc_req:
                    custom_checklist["tier2_financial_funds"][0]["detail"] += f" (Yêu cầu tối thiểu tại {c_en}: €{inc_req:,}/tháng)."
                if dn_data.get("tax_regime"):
                    custom_checklist["tier2_financial_funds"].append({
                        "item": "Chế độ thuế & Tình trạng cư trú thuế",
                        "detail": f"Chính sách thuế: {dn_data['tax_regime']}."
                    })
                    
        elif arch_id == "passive_income":
            if fip_data:
                inc_req = fip_data.get("min_monthly_income_eur")
                if inc_req:
                    custom_checklist["tier2_financial_funds"][0]["detail"] += f" (Yêu cầu tại {c_en}: €{inc_req:,}/tháng; Yêu cầu tiết kiệm: {fip_data.get('savings_required')})."
            if "spain" in c_en.lower():
                custom_checklist["tier2_financial_funds"].append({
                    "item": "Chuẩn IPREM Tây Ban Nha (Non-Lucrative Visa)",
                    "detail": "Yêu cầu 400% chuẩn IPREM hàng tháng (~€2,400/tháng cho đương đơn chính + 100% IPREM (~€600/tháng) cho mỗi người phụ thuộc)."
                })

        prog_obj = {
            "id": f"{c_slug}_{idx}",
            "program_name": p_name,
            "category": cat_str,
            "archetype_id": arch_id,
            "archetype_name": arch_schema["name_vi"],
            "country_en": c_en,
            "country_vi": c_meta["country_vi"],
            "country_slug": c_slug,
            "financial_requirement_text": p["financial_requirement"],
            "min_investment_eur": inv_eur,
            "min_monthly_income_eur": inc_eur,
            "min_physical_stay_days_per_year": stay_days,
            "processing_time": p["processing_time"],
            "timeline_pr": p["timeline_pr"],
            "timeline_citizenship": p["timeline_citizenship"],
            "timeline_pr_years": pr_years,
            "timeline_citizenship_years": cit_years,
            "language_requirement": p["language_requirement"],
            "main_conditions": p["conditions"],
            "checklist": custom_checklist
        }
        enriched_progs.append(prog_obj)
        master_programs_list.append(prog_obj)

    country_dossier = {
        "country_en": c_en,
        "country_vi": c_meta["country_vi"],
        "slug": c_slug,
        "overview": c_meta,
        "difficulty_and_stats": c_diff,
        "recent_policy_changes": c_changes,
        "official_references": c_refs,
        "programs_count": len(enriched_progs),
        "programs": enriched_progs
    }
    
    all_enriched_countries[c_slug] = country_dossier
    
    # Write country JSON
    json_path = os.path.join(COUNTRIES_DIR, f"{c_slug}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(country_dossier, f, ensure_ascii=False, indent=2)
        
    # Write country Markdown Dossier
    md_path = os.path.join(COUNTRIES_DIR, f"{c_slug}.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# Hồ Sơ Định Cư Toàn Diện: {c_meta['country_vi']} ({c_en})\n\n")
        f.write(f"> **Tình trạng:** {c_meta['eu_schengen_status']} | **Mức độ khó:** {c_meta['difficulty_rating']} | **Website chính thức:** [{c_meta['official_portal']}](https://{c_meta['official_portal'].split('/')[0].strip()})\n\n")
        f.write(f"## 1. Tổng Quan Di Trú & Chỉ Số Quốc Gia\n\n")
        f.write(f"- **Điểm hội nhập MIPEX:** {c_meta['mipex_score']}/100\n")
        f.write(f"- **Tỷ lệ từ chối visa:** {c_meta['visa_refusal_rate']}%\n")
        if c_diff:
            f.write(f"- **Thời gian xử lý trung bình:** {c_diff.get('processing_months', 'N/A')} tháng\n")
            f.write(f"- **Lộ trình Thường trú nhân (PR):** {c_diff.get('years_to_pr', 'N/A')} năm\n")
            f.write(f"- **Lộ trình Quốc tịch:** {c_diff.get('years_to_citizenship', 'N/A')} năm\n")
            f.write(f"- **Ghi chú đánh giá:** {c_diff.get('notes', '')}\n")
        f.write(f"\n---\n\n")
        
        if c_changes:
            f.write("## 2. Cập Nhật Chính Sách Mới Nhất 2025 - 2026\n\n")
            for ch in c_changes:
                f.write(f"- **[{ch.get('time', '')}] {ch.get('change', '')}**\n")
                f.write(f"  - *Tác động:* {ch.get('impact', '')}\n")
                f.write(f"  - *Trạng thái:* {ch.get('status', '')} | *Chi tiết:* {ch.get('detail', '')}\n\n")
            f.write("---\n\n")

        f.write(f"## 3. Danh Sách {len(enriched_progs)} Chương Trình / Loại Visa Định Cư\n\n")
        for p in enriched_progs:
            f.write(f"### 📌 {p['program_name']} ({p['archetype_name']})\n\n")
            f.write(f"- **Phân loại:** `{p['category']}`\n")
            f.write(f"- **Yêu cầu tài chính:** {p['financial_requirement_text']}\n")
            f.write(f"- **Thời gian xử lý:** {p['processing_time']}\n")
            f.write(f"- **Thời gian đến Thường trú nhân (PR):** {p['timeline_pr']}\n")
            f.write(f"- **Thời gian đến Quốc tịch (Citizenship):** {p['timeline_citizenship']}\n")
            f.write(f"- **Yêu cầu cư trú thực tế:** Tối thiểu {p['min_physical_stay_days_per_year']} ngày/năm\n")
            f.write(f"- **Yêu cầu ngôn ngữ:** {p['language_requirement']}\n")
            f.write(f"- **Điều kiện tiên quyết:** {p['main_conditions']}\n\n")
            
            f.write("#### 📋 Bộ Checklist Hồ Sơ Cần Chuẩn Bị (5 Nhóm Tiêu Chuẩn)\n\n")
            chk = p["checklist"]
            
            f.write("**Nhóm 1: Nhân Thân & Hộ Tịch (Civil & Identity)**\n")
            for item in chk["tier1_civil_identity"]:
                f.write(f"- [ ] **{item['item']}**: {item['detail']}\n")
            f.write("\n")
            
            f.write("**Nhóm 2: Năng Lực Tài Chính & Nguồn Tiền (Financial & Source of Funds)**\n")
            for item in chk["tier2_financial_funds"]:
                f.write(f"- [ ] **{item['item']}**: {item['detail']}\n")
            f.write("\n")
            
            f.write("**Nhóm 3: Hồ Sơ Chuyên Biệt Theo Diện (Specialized Program Documents)**\n")
            for item in chk["tier3_specialized_investment"]:
                f.write(f"- [ ] **{item['item']}**: {item['detail']}\n")
            f.write("\n")
            
            f.write("**Nhóm 4: Chỗ Ở & Bảo Hiểm Y Tế (Accommodation & Health Insurance)**\n")
            for item in chk["tier4_accommodation_health"]:
                f.write(f"- [ ] **{item['item']}**: {item['detail']}\n")
            f.write("\n")
            
            f.write("**Nhóm 5: Quy Chuẩn Nộp & Hợp Pháp Hoá Lãnh Sự (Legalization & Submission)**\n")
            for item in chk["tier5_legalization_submission"]:
                f.write(f"- [ ] **{item['item']}**: {item['detail']}\n")
            f.write("\n---\n\n")

        if c_refs:
            f.write("## 4. Nguồn Tham Khảo & Cổng Thông Tin Chính Thức\n\n")
            for ref in c_refs:
                f.write(f"- **{ref['name']}** ({ref['category']}): [{ref['url']}](https://{ref['url'].split('/')[0].strip()}) - {ref['description']}\n")
            f.write("\n")

# Write Master Database JSON
master_db_path = os.path.join(DATA_DIR, "eu_immigration_master.json")
with open(master_db_path, 'w', encoding='utf-8') as f:
    json.dump({
        "generated_date": "2026-11-14",
        "total_countries": len(all_enriched_countries),
        "total_programs": len(master_programs_list),
        "countries": all_enriched_countries,
        "all_programs": master_programs_list
    }, f, ensure_ascii=False, indent=2)

# Write Archetypes & Checklists JSON
archetypes_path = os.path.join(DATA_DIR, "archetypes_checklists.json")
with open(archetypes_path, 'w', encoding='utf-8') as f:
    json.dump(ARCHETYPES, f, ensure_ascii=False, indent=2)

print(f"Successfully processed {len(all_enriched_countries)} countries and {len(master_programs_list)} visa programs.")
print(f"Files created in {COUNTRIES_DIR}/ and {DATA_DIR}/")
