"""
matching_engine.py
Module evaluating client profiles against EU/Schengen immigration programs.
Calculates multidimensional compatibility scores (0-100%) and returns tailored pros/cons and checklists.
"""

from typing import Dict, List, Any

def evaluate_client_profile(client_profile: Dict[str, Any], programs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Evaluates client profile against all visa programs.
    Returns sorted list of evaluated programs with match scores, pros, and caveats.
    """
    budget = float(client_profile.get("budget_eur", 0))
    monthly_income = float(client_profile.get("monthly_income_eur", 0))
    income_type = client_profile.get("income_type", "local_job_offer") # remote_work, passive, local_job_offer, business_owner, investment_capital
    physical_stay = client_profile.get("physical_stay_capability", "full_residency") # minimal, flexible, full_residency
    education = client_profile.get("education_level", "bachelor") # high_school, bachelor, master_phd
    is_stem = bool(client_profile.get("stem_tech_field", False))
    primary_goal = client_profile.get("primary_goal", "citizenship_passport") # citizenship_passport, pr_permanent_residency, schengen_mobility, education_kids, expand_business
    family = client_profile.get("family_composition", "family_with_kids") # single, couple, family_with_kids, multi_generational
    lang_willing = client_profile.get("language_willingness", "willing_to_learn") # english_only, willing_to_learn

    results = []

    for prog in programs:
        arch_id = prog.get("archetype_id", "")
        country_en = prog.get("country_en", "")
        country_vi = prog.get("country_vi", "")
        p_name = prog.get("program_name", "")
        min_inv = float(prog.get("min_investment_eur", 0))
        min_inc = float(prog.get("min_monthly_income_eur", 0))
        req_stay = int(prog.get("min_physical_stay_days_per_year", 183))
        cit_years = int(prog.get("timeline_citizenship_years", 10))
        pr_years = int(prog.get("timeline_pr_years", 5))

        financial_score = 0
        stay_score = 0
        education_score = 0
        family_score = 100
        goal_score = 0

        pros = []
        caveats = []

        # 1. Financial Score (Weight 35)
        if arch_id == "golden_visa":
            if budget >= min_inv and min_inv > 0:
                financial_score = 100
                pros.append(f"Ngân sách đầu tư (€{budget:,.0f}) đáp ứng hoàn hảo mức tối thiểu (€{min_inv:,.0f}).")
            elif budget >= min_inv * 0.8:
                financial_score = 70
                caveats.append(f"Ngân sách hiện tại (€{budget:,.0f}) gần chạm mức tối thiểu (€{min_inv:,.0f}), cần bổ sung thêm vốn dự phòng.")
            else:
                financial_score = max(0, 100 - (min_inv - budget) / 5000)
                caveats.append(f"Ngân sách đầu tư chưa đủ (yêu cầu tối thiểu €{min_inv:,.0f}).")

        elif arch_id == "digital_nomad":
            if income_type == "remote_work" or income_type == "business_owner":
                if monthly_income >= min_inc:
                    financial_score = 100
                    pros.append(f"Thu nhập từ xa (€{monthly_income:,.0f}/tháng) vượt ngưỡng yêu cầu (€{min_inc:,.0f}/tháng).")
                elif monthly_income >= min_inc * 0.8:
                    financial_score = 75
                    caveats.append(f"Thu nhập từ xa (€{monthly_income:,.0f}/tháng) sát ngưỡng tối thiểu (€{min_inc:,.0f}/tháng).")
                else:
                    financial_score = 40
                    caveats.append(f"Thu nhập từ xa chưa đạt mức quy định (€{min_inc:,.0f}/tháng).")
            else:
                financial_score = 30
                caveats.append("Diện Digital Nomad yêu cầu hợp đồng lao động từ xa hoặc hợp đồng dịch vụ trực tuyến với khách hàng ngoài nước sở tại.")

        elif arch_id == "passive_income":
            if income_type == "passive":
                if monthly_income >= min_inc:
                    financial_score = 100
                    pros.append(f"Nguồn thu nhập thụ động (€{monthly_income:,.0f}/tháng) chứng minh dòng tiền bền vững xuất sắc.")
                else:
                    financial_score = 60
                    caveats.append(f"Thu nhập thụ động chưa đủ mức khuyến nghị (€{min_inc:,.0f}/tháng).")
            else:
                financial_score = 25
                caveats.append("Diện này bắt buộc thu nhập phải là thụ động (tiền thuê nhà, cổ tức, hưu trí), không chấp nhận lương đi làm công.")

        elif arch_id == "blue_card":
            # Doesn't require investment capital, requires employment/qualifications
            if income_type == "local_job_offer":
                financial_score = 100
                pros.append("Có cơ hội việc làm tại EU; không yêu cầu vốn đầu tư lớn ban đầu.")
            else:
                financial_score = 80
                pros.append("Không yêu cầu vốn đầu tư; cần có Thư mời làm việc (Job Offer) từ doanh nghiệp sở tại.")

        elif arch_id == "startup_entrepreneur":
            if budget >= 30000:
                financial_score = 100
                pros.append("Nguồn vốn sẵn sàng đáp ứng yêu cầu vận hành doanh nghiệp khởi nghiệp.")
            else:
                financial_score = 65
                caveats.append("Cần tối thiểu €30,000 - €50,000 vốn khởi nghiệp và chứng minh chi phí sinh hoạt.")

        # 2. Physical Stay Score (Weight 25)
        if physical_stay == "minimal": # 0-14 days/year
            if req_stay <= 14:
                stay_score = 100
                pros.append(f"Yêu cầu cư trú thực tế cực kỳ linh hoạt (chỉ {req_stay} ngày/năm), không ảnh hưởng công việc tại Việt Nam.")
            else:
                stay_score = 20
                caveats.append(f"Chương trình yêu cầu cư trú thực tế tối thiểu {req_stay} ngày/năm (183 ngày/năm). Khách hàng không thể ở thường trực sẽ khó duy trì visa.")
        elif physical_stay == "flexible": # 1-3 months
            if req_stay <= 90:
                stay_score = 100
                pros.append("Thời gian cư trú yêu cầu phù hợp với khả năng thu xếp thời gian của khách hàng.")
            else:
                stay_score = 55
                caveats.append(f"Chương trình yêu cầu cư trú tối thiểu {req_stay} ngày/năm để gia hạn và xin PR.")
        else: # full_residency (>183 days)
            stay_score = 100
            pros.append("Khách hàng sẵn sàng sang sinh sống thực tế, đáp ứng trọn vẹn điều kiện cư trú để lên Thường trú nhân và Quốc tịch.")

        # 3. Education & Skill Score (Weight 15)
        if arch_id == "blue_card":
            if education in ["bachelor", "master_phd"]:
                education_score = 100
                pros.append(f"Bằng cấp ({education.upper()}) đáp ứng đầy đủ điều kiện tiên quyết của EU Blue Card.")
                if is_stem:
                    pros.append("Thuộc nhóm ngành ưu tiên STEM/CNTT: Ngưỡng lương xét duyệt được giảm đáng kể.")
            else:
                education_score = 10
                caveats.append("EU Blue Card bắt buộc phải có bằng tốt nghiệp Đại học (hoặc 3 năm kinh nghiệm CNTT bậc cao theo luật mới).")
        else:
            education_score = 100

        # 4. Family Dependents Score (Weight 10)
        if family == "multi_generational":
            if country_en.lower() in ["greece", "malta", "cyprus"] and arch_id == "golden_visa":
                family_score = 100
                pros.append("Chính sách 'Tứ thân phụ mẫu': Cho phép bảo lãnh cả cha mẹ 2 bên và con cái phụ thuộc trong cùng 1 bộ hồ sơ.")
            elif arch_id in ["golden_visa", "passive_income"]:
                family_score = 85
                pros.append("Có thể bảo lãnh gia đình (vợ/chồng, con cái phụ thuộc).")
            else:
                family_score = 65
                caveats.append("Diện này thường chỉ bảo lãnh vợ/chồng và con cái dưới 18 tuổi; khó bảo lãnh cha mẹ trực tiếp.")
        else:
            family_score = 100
            pros.append("Hồ sơ bảo lãnh gia đình cơ bản (vợ/chồng và con cái) hoàn toàn thuận lợi.")

        # 5. Goal Alignment Score (Weight 15)
        if primary_goal == "citizenship_passport":
            if cit_years <= 5:
                goal_score = 100
                pros.append(f"Lộ trình nhập Quốc tịch Châu Âu cực nhanh: Chỉ {cit_years} năm cư trú (áp dụng ưu thế luật quốc tịch mới).")
            elif cit_years <= 7:
                goal_score = 80
                pros.append(f"Lộ trình nhập tịch tiêu chuẩn {cit_years} năm.")
            else:
                goal_score = 50
                caveats.append(f"Thời gian chờ nhập quốc tịch khá dài ({cit_years} năm).")

        elif primary_goal == "pr_permanent_residency":
            if pr_years <= 3:
                goal_score = 100
                pros.append(f"Thời gian lấy Thường trú nhân (PR) siêu tốc: Chỉ {pr_years} năm (như Blue Card Đức rút ngắn còn 21-27 tháng).")
            else:
                goal_score = 85
                pros.append(f"Lộ trình lên Thường trú nhân (PR) an toàn sau {pr_years} năm.")

        elif primary_goal == "schengen_mobility":
            goal_score = 100
            pros.append("Hưởng quyền tự do đi lại miễn thị thực trong toàn bộ 29 quốc gia thuộc khối Schengen.")

        elif primary_goal == "education_kids":
            if stay_score >= 80:
                goal_score = 100
                pros.append("Con cái được hưởng nền giáo dục chuẩn châu Âu, miễn 100% học phí tại hệ thống trường công lập địa phương.")
            else:
                goal_score = 70
                caveats.append("Để con cái theo học trường công miễn phí, gia đình cần sinh sống thực tế tại nước sở tại.")

        elif primary_goal == "expand_business":
            if arch_id in ["startup_entrepreneur", "golden_visa"]:
                goal_score = 100
                pros.append("Mở rộng thị trường kinh doanh và tiếp cận mạng lưới thương mại toàn khối Liên minh Châu Âu (EU Single Market).")
            else:
                goal_score = 70

        # Language caveat check
        if lang_willing == "english_only":
            if "b1" in prog.get("language_requirement", "").lower() or "a2" in prog.get("language_requirement", "").lower():
                caveats.append(f"Yêu cầu ngoại ngữ: {prog.get('language_requirement')}. Cần chuẩn bị học tiếng bản địa cơ bản khi xin PR/Quốc tịch.")

        # Calculate Total Weighted Score
        total_score = (
            financial_score * 0.35 +
            stay_score * 0.25 +
            education_score * 0.15 +
            family_score * 0.10 +
            goal_score * 0.15
        )

        # Floor and Ceiling
        total_score = max(5.0, min(99.0, total_score))

        # Determine Tier
        if total_score >= 85:
            tier = "Xuất Sắc (85-100%)"
            badge_color = "green"
        elif total_score >= 70:
            tier = "Rất Phù Hợp (70-84%)"
            badge_color = "blue"
        elif total_score >= 55:
            tier = "Khả Thi (55-69%)"
            badge_color = "orange"
        else:
            tier = "Cân Nhắc (<55%)"
            badge_color = "red"

        results.append({
            "program_id": prog.get("id"),
            "program_name": p_name,
            "category": prog.get("category"),
            "archetype_id": arch_id,
            "archetype_name": prog.get("archetype_name"),
            "country_en": country_en,
            "country_vi": country_vi,
            "country_slug": prog.get("country_slug"),
            "match_score": round(total_score, 1),
            "match_tier": tier,
            "badge_color": badge_color,
            "breakdown": {
                "financial_score": round(financial_score, 1),
                "stay_score": round(stay_score, 1),
                "education_score": round(education_score, 1),
                "family_score": round(family_score, 1),
                "goal_score": round(goal_score, 1)
            },
            "pros": pros[:4],
            "caveats": caveats[:3],
            "program_details": prog
        })

    # Sort descending by match score
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results
