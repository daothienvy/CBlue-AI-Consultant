"""
app.py
CÔNG CỤ PHÂN TÍCH & MATCH CHƯƠNG TRÌNH ĐỊNH CƯ CHÂU ÂU (EU & SCHENGEN IMMIGRATION MATCHING TOOL)
Hệ thống Knowledge Base 31 quốc gia EU/Schengen, 79+ chương trình định cư và Bộ Checklist hồ sơ 5 nhóm tiêu chuẩn.
"""

import os
import json
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from matching_engine import evaluate_client_profile
from report_generator import generate_html_report, generate_pdf_report

# Page config
st.set_page_config(
    page_title="EU Immigration Matching Tool & Knowledge Base 2026",
    page_icon="🇪🇺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        padding: 24px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: #f8fafc;
        margin: 0;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #94a3b8;
        margin: 6px 0 0 0;
        font-size: 14px;
    }
    .match-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: transform 0.2s;
    }
    .match-score-badge {
        font-size: 24px;
        font-weight: 800;
        padding: 6px 14px;
        border-radius: 8px;
        display: inline-block;
    }
    .score-green { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
    .score-blue { background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }
    .score-orange { background: #ffedd5; color: #c2410c; border: 1px solid #fed7aa; }
    .score-red { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        font-weight: 600;
        border-radius: 6px 6px 0 0;
    }
</style>
""", unsafe_allow_html=True)

# Load Master Database
DATA_DIR = "data"
MASTER_FILE = os.path.join(DATA_DIR, "eu_immigration_master.json")
ARCHETYPES_FILE = os.path.join(DATA_DIR, "archetypes_checklists.json")
COUNTRIES_DIR = os.path.join(DATA_DIR, "countries")

@st.cache_data
def load_data():
    with open(MASTER_FILE, "r", encoding="utf-8") as f:
        master_data = json.load(f)
    with open(ARCHETYPES_FILE, "r", encoding="utf-8") as f:
        archetypes_data = json.load(f)
    return master_data, archetypes_data

master_data, archetypes_data = load_data()
all_programs = master_data["all_programs"]
all_countries = master_data["countries"]

# Header
st.markdown("""
<div class="main-header">
    <h1>🇪🇺 CÔNG CỤ PHÂN TÍCH & MATCH CHƯƠNG TRÌNH ĐỊNH CƯ CHÂU ÂU 2026</h1>
    <p>Cơ sở dữ liệu 31 Quốc gia EU & Schengen | 79 Chương trình Định cư | Chuẩn hóa 5 Nhóm Hồ Sơ Chi Tiết</p>
</div>
""", unsafe_allow_html=True)

# Tabs Navigation
tab_wizard, tab_filter, tab_explorer, tab_compare, tab_archetypes = st.tabs([
    "🎯 Khảo Sát & Match Khách Hàng",
    "⚡ Bộ Lọc Chuyên Viên (Matrix)",
    "🌍 Tra Cứu 31 Nước & Checklist",
    "⚖️ So Sánh Chương Trình",
    "📚 Chuẩn Hóa 5 Diện Visa"
])

# ==============================================================================
# TAB 1: CLIENT SMART WIZARD
# ==============================================================================
with tab_wizard:
    st.markdown("### 📋 Bảng Khảo Sát Đánh Giá Hồ Sơ & Nhu Cầu Khách Hàng")
    st.caption("Nhập các thông số thực tế của khách hàng để hệ thống tính toán điểm tương thích (Match Score %) và đề xuất các chương trình tối ưu nhất kèm bộ hồ sơ cần chuẩn bị.")

    with st.form("client_intake_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 1. Thông Tin Chung & Năng Lực Tài Chính")
            client_name = st.text_input("Họ & Tên khách hàng / Mã hồ sơ:", value="Khách Hàng Mẫu A")
            
            budget_eur = st.number_input(
                "Ngân sách tài chính khả dụng cho việc định cư (€ EUR):",
                min_value=0,
                max_value=5000000,
                value=250000,
                step=25000,
                help="Số tiền vốn sẵn sàng đầu tư, ký quỹ hoặc chi trả cho chi phí hồ sơ và sinh hoạt."
            )

            monthly_income_eur = st.number_input(
                "Thu nhập chứng minh hàng tháng (€ EUR/tháng):",
                min_value=0,
                max_value=100000,
                value=3500,
                step=500,
                help="Thu nhập từ xa, lương công ty, cho thuê BĐS, cổ tức, hoặc lương hưu."
            )

            income_type = st.selectbox(
                "Bản chất / Nguồn gốc thu nhập chính:",
                options=[
                    ("investment_capital", "💰 Vốn đầu tư tích lũy sẵn có (Không cần đi làm, chỉ đầu tư)"),
                    ("remote_work", "💻 Lương làm việc từ xa / Freelancer quốc tế / Online Business"),
                    ("passive", "🏡 Thu nhập thụ động bền vững (Cho thuê nhà, cổ tức, lương hưu)"),
                    ("local_job_offer", "👔 Lao động kỹ năng cao / Có bằng ĐH / Có Job Offer tại EU"),
                    ("business_owner", "🚀 Chủ doanh nghiệp / Khởi nghiệp mở công ty tại EU")
                ],
                format_func=lambda x: x[1]
            )[0]

            primary_goal = st.selectbox(
                "Mục tiêu ưu tiên hàng đầu của gia đình:",
                options=[
                    ("citizenship_passport", "🛂 Nhập Quốc tịch / Lấy Hộ chiếu EU nhanh nhất"),
                    ("pr_permanent_residency", "🛡️ Lấy Thường trú nhân (PR) an toàn, dài hạn"),
                    ("schengen_mobility", "✈️ Tự do đi lại 29 nước Schengen cho cả gia đình"),
                    ("education_kids", "🎓 Cho con cái học trường công miễn phí / an sinh tốt"),
                    ("expand_business", "🏢 Mở rộng kinh doanh & đầu tư vào thị trường EU")
                ],
                format_func=lambda x: x[1]
            )[0]

        with col2:
            st.markdown("##### 2. Điều Kiện Cư Trú & Thành Viên Đi Kèm")
            physical_stay = st.selectbox(
                "Khả năng cư trú thực tế tại nước sở tại:",
                options=[
                    ("minimal", "⏳ Tối thiểu (Chỉ sang 0 - 14 ngày/năm để giữ thẻ, vẫn ở VN làm việc)"),
                    ("flexible", "✈️ Linh hoạt (Có thể sang ở 1 - 3 tháng/năm)"),
                    ("full_residency", "🏠 Định cư thực tế (Sẵn sàng ở >183 ngày/năm để sinh sống)")
                ],
                format_func=lambda x: x[1]
            )[0]

            family_comp = st.selectbox(
                "Thành phần gia đình đi cùng trong hồ sơ:",
                options=[
                    ("single", "👤 Đi 1 mình (Độc thân)"),
                    ("couple", "👫 Vợ / Chồng"),
                    ("family_with_kids", "👨‍👩‍👧‍👦 Vợ chồng + Con cái phụ thuộc (<18 hoặc <26t)"),
                    ("multi_generational", "👨‍👩‍👧‍👦👵 Vợ chồng + Con cái + Bố mẹ 2 bên (Tứ thân phụ mẫu)")
                ],
                format_func=lambda x: x[1]
            )[0]

            col_edu1, col_edu2 = st.columns(2)
            with col_edu1:
                education_level = st.selectbox(
                    "Trình độ học vấn cao nhất:",
                    options=[
                        ("high_school", "Tốt nghiệp THPT / Trung cấp"),
                        ("bachelor", "Tốt nghiệp Đại học"),
                        ("master_phd", "Thạc sĩ / Tiến sĩ")
                    ],
                    format_func=lambda x: x[1]
                )[0]

            with col_edu2:
                is_stem = st.checkbox("Ngành CNTT, Kỹ thuật, Khoa học, Y tế (STEM)?", value=False)

            lang_willingness = st.selectbox(
                "Khả năng ngoại ngữ & Sẵn sàng học tiếng bản địa:",
                options=[
                    ("willing_to_learn", "📖 Sẵn sàng học tiếng bản địa cơ bản (A2/B1) để thi quốc tịch"),
                    ("english_only", "🗣️ Chỉ sử dụng tiếng Anh / Không muốn học tiếng địa phương")
                ],
                format_func=lambda x: x[1]
            )[0]

        submit_match = st.form_submit_button("🚀 PHÂN TÍCH & MATCH CHƯƠNG TRÌNH PHÙ HỢP", use_container_width=True)

    if submit_match or "last_matches" in st.session_state:
        if submit_match:
            profile = {
                "client_name": client_name,
                "budget_eur": budget_eur,
                "monthly_income_eur": monthly_income_eur,
                "income_type": income_type,
                "physical_stay_capability": physical_stay,
                "education_level": education_level,
                "stem_tech_field": is_stem,
                "primary_goal": primary_goal,
                "family_composition": family_comp,
                "language_willingness": lang_willingness
            }
            matches = evaluate_client_profile(profile, all_programs)
            st.session_state["last_profile"] = profile
            st.session_state["last_matches"] = matches
        else:
            profile = st.session_state["last_profile"]
            matches = st.session_state["last_matches"]

        top_matches = matches[:5]

        st.markdown("---")
        st.markdown(f"### 🏆 KẾT QUẢ ĐÁNH GIÁ: TOP CHƯƠNG TRÌNH TỐI ƯU CHO {profile['client_name'].upper()}")
        st.caption(f"Đã phân tích 79 chương trình định cư trên 31 quốc gia EU & Schengen dựa trên 5 chiều tiêu chí.")

        # Top 3 Columns Cards
        cols_top = st.columns(3)
        for i in range(min(3, len(top_matches))):
            m = top_matches[i]
            p = m["program_details"]
            score = m["match_score"]
            badge_class = "score-green" if score >= 85 else ("score-blue" if score >= 70 else "score-orange")

            with cols_top[i]:
                st.markdown(f"""
                <div class="match-card">
                    <span style="font-size:12px; font-weight:700; color:#2563eb;">LỰA CHỌN #{i+1}</span>
                    <h4 style="margin:4px 0; color:#0f172a;">{m['country_vi']}</h4>
                    <p style="margin:0; font-size:14px; font-weight:600; color:#334155;">{m['program_name']}</p>
                    <span style="font-size:12px; color:#64748b;">{m['archetype_name']}</span>
                    <div style="margin:12px 0;">
                        <span class="match-score-badge {badge_class}">{score}%</span>
                        <span style="font-size:12px; color:#64748b; margin-left:6px;">Tương thích</span>
                    </div>
                    <div style="font-size:12px; color:#334155;">
                        <div>💶 <b>Tài chính:</b> {p['financial_requirement_text']}</div>
                        <div>✈️ <b>Cư trú:</b> {p['min_physical_stay_days_per_year']} ngày/năm</div>
                        <div>🛂 <b>Lấy Quốc tịch:</b> {p['timeline_citizenship']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Detailed breakdown of Top Recommended
        st.markdown("#### 🔍 Chi Tiết Phân Tích & Bộ Hồ Sơ Yêu Cầu")

        for idx, m in enumerate(top_matches, 1):
            p = m["program_details"]
            with st.expander(f"#{idx}. {m['country_vi']} ({m['country_en']}) — {m['program_name']} | Độ phù hợp: {m['match_score']}% ({m['match_tier']})", expanded=(idx==1)):
                col_d1, col_d2 = st.columns([1, 1])

                with col_d1:
                    st.markdown("##### 📊 Điểm Phân Tích Thành Phần")
                    bd = m["breakdown"]
                    st.progress(bd["financial_score"] / 100, text=f"Tài chính & Thu nhập: {bd['financial_score']}%")
                    st.progress(bd["stay_score"] / 100, text=f"Điều kiện cư trú: {bd['stay_score']}%")
                    st.progress(bd["education_score"] / 100, text=f"Bằng cấp & Kỹ năng: {bd['education_score']}%")
                    st.progress(bd["goal_score"] / 100, text=f"Phù hợp mục tiêu: {bd['goal_score']}%")

                    st.markdown("##### ✅ Ưu Điểm Phù Hợp Với Khách Hàng")
                    for pro in m["pros"]:
                        st.markdown(f"- ✅ **{pro}**")

                with col_d2:
                    st.markdown("##### 📌 Thông Số Chương Trình")
                    st.write(f"- **Phân loại:** {m['archetype_name']} (`{p['category']}`)")
                    st.write(f"- **Chi phí yêu cầu:** {p['financial_requirement_text']}")
                    st.write(f"- **Thời gian xử lý:** {p['processing_time']}")
                    st.write(f"- **Thời gian đến Thường trú nhân (PR):** {p['timeline_pr']}")
                    st.write(f"- **Thời gian đến Quốc tịch:** {p['timeline_citizenship']}")
                    st.write(f"- **Yêu cầu ngôn ngữ:** {p['language_requirement']}")
                    st.write(f"- **Điều kiện tiên quyết:** {p['main_conditions']}")

                    if m["caveats"]:
                        st.markdown("##### ⚠️ Điểm Cần Lưu Ý")
                        for con in m["caveats"]:
                            st.markdown(f"- ⚠️ *{con}*")

                st.markdown("---")
                st.markdown(f"##### 📋 Bộ Checklist Hồ Sơ Cần Chuẩn Bị: {m['program_name']}")
                
                chk = p["checklist"]
                t1, t2, t3, t4, t5 = st.tabs([
                    "1. Nhân Thân & Hộ Tịch",
                    "2. Tài Chính & Nguồn Tiền",
                    "3. Nghiệp Vụ Theo Diện",
                    "4. Chỗ Ở & Bảo Hiểm",
                    "5. Nộp & Hợp Pháp Hóa"
                ])

                with t1:
                    for item in chk["tier1_civil_identity"]:
                        st.checkbox(f"**{item['item']}**: {item['detail']}", key=f"c1_{m['program_id']}_{item['item'][:15]}")
                with t2:
                    for item in chk["tier2_financial_funds"]:
                        st.checkbox(f"**{item['item']}**: {item['detail']}", key=f"c2_{m['program_id']}_{item['item'][:15]}")
                with t3:
                    for item in chk["tier3_specialized_investment"]:
                        st.checkbox(f"**{item['item']}**: {item['detail']}", key=f"c3_{m['program_id']}_{item['item'][:15]}")
                with t4:
                    for item in chk["tier4_accommodation_health"]:
                        st.checkbox(f"**{item['item']}**: {item['detail']}", key=f"c4_{m['program_id']}_{item['item'][:15]}")
                with t5:
                    for item in chk["tier5_legalization_submission"]:
                        st.checkbox(f"**{item['item']}**: {item['detail']}", key=f"c5_{m['program_id']}_{item['item'][:15]}")

        # Action: Export Report
        st.markdown("---")
        st.markdown("### 📤 Xuất Báo Cáo Tư Vấn Cá Nhân Hóa Cho Khách Hàng")
        col_btn1, col_btn2 = st.columns(2)

        html_report = generate_html_report(profile, top_matches)
        pdf_filename = f"Bao_Cao_Dinh_Cu_{profile['client_name'].replace(' ', '_')}.pdf"
        pdf_path = os.path.join(DATA_DIR, pdf_filename)
        generate_pdf_report(profile, top_matches, pdf_path)

        with col_btn1:
            with open(pdf_path, "rb") as f_pdf:
                st.download_button(
                    label="📥 Tải Báo Cáo PDF Chuẩn In Ấn",
                    data=f_pdf,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    use_container_width=True
                )

        with col_btn2:
            st.download_button(
                label="📄 Tải Báo Cáo Định Dạng HTML / Web",
                data=html_report,
                file_name=f"Bao_Cao_Dinh_Cu_{profile['client_name'].replace(' ', '_')}.html",
                mime="text/html",
                use_container_width=True
            )

        with st.expander("👁️ Xem Trước Bản In Báo Cáo Trực Tuyến (Print Preview)"):
            components.html(html_report, height=650, scrolling=True)


# ==============================================================================
# TAB 2: ADVISOR QUICK MATRIX (FILTER TABLE)
# ==============================================================================
with tab_filter:
    st.markdown("### ⚡ Bộ Lọc Chuyên Viên Tư Vấn — Ma Trận 79 Chương Trình Định Cư")
    st.caption("Bộ công cụ tra cứu đa chiều dành cho chuyên viên: lọc tức thì theo ngân sách, loại visa, thời gian cư trú, quốc gia và trích xuất dữ liệu.")

    # Filter Controls
    fc1, fc2, fc3, fc4 = st.columns(4)

    with fc1:
        country_filter = st.selectbox(
            "Lọc theo Quốc Gia:",
            options=["Tất cả 31 Quốc Gia"] + sorted(list(set(p["country_vi"] for p in all_programs)))
        )

    with fc2:
        arch_filter = st.selectbox(
            "Lọc theo Phân Loại Visa:",
            options=["Tất cả các diện"] + [v["name_vi"] for v in archetypes_data.values()]
        )

    with fc3:
        max_budget = st.slider(
            "Ngân sách đầu tư tối đa (€ EUR):",
            min_value=0,
            max_value=1000000,
            value=1000000,
            step=50000,
            format="€%d"
        )

    with fc4:
        stay_filter = st.selectbox(
            "Yêu cầu cư trú thực tế:",
            options=["Tất cả", "Linh hoạt (<= 14 ngày/năm)", "Định cư thực tế (> 180 ngày/năm)"]
        )

    # Filter data
    filtered_progs = []
    for p in all_programs:
        if country_filter != "Tất cả 31 Quốc Gia" and p["country_vi"] != country_filter:
            continue
        if arch_filter != "Tất cả các diện" and p["archetype_name"] != arch_filter:
            continue
        if p["min_investment_eur"] > max_budget:
            continue
        if stay_filter == "Linh hoạt (<= 14 ngày/năm)" and p["min_physical_stay_days_per_year"] > 14:
            continue
        if stay_filter == "Định cư thực tế (> 180 ngày/năm)" and p["min_physical_stay_days_per_year"] <= 14:
            continue
        filtered_progs.append(p)

    st.markdown(f"**Tìm thấy {len(filtered_progs)} chương trình phù hợp:**")

    # Table view
    table_rows = []
    for p in filtered_progs:
        table_rows.append({
            "Quốc Gia": f"{p['country_vi']} ({p['country_en']})",
            "Tên Chương Trình / Visa": p["program_name"],
            "Phân Loại": p["archetype_name"],
            "Yêu Cầu Tài Chính": p["financial_requirement_text"],
            "Cư Trú (ngày/năm)": p["min_physical_stay_days_per_year"],
            "Thời Gian Xử Lý": p["processing_time"],
            "Lộ Trình PR": p["timeline_pr"],
            "Lộ Trình Quốc Tịch": p["timeline_citizenship"],
            "Ngoại Ngữ": p["language_requirement"]
        })

    df_filtered = pd.DataFrame(table_rows)
    st.dataframe(df_filtered, use_container_width=True, height=450)

    # Export to Excel
    csv_data = df_filtered.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        "📥 Tải Bảng Kết Quả Này Dưới Dạng CSV/Excel",
        data=csv_data,
        file_name="Ma_Tran_Dinh_Cu_EU.csv",
        mime="text/csv"
    )

    # Quick program checklist drawer
    st.markdown("---")
    st.markdown("##### 📌 Tra Cứu Nhanh Checklist Hồ Sơ Cho 1 Chương Trình")
    selected_p_name = st.selectbox(
        "Chọn chương trình để mở chi tiết 5 nhóm hồ sơ:",
        options=[f"{p['country_vi']} - {p['program_name']}" for p in filtered_progs]
    )

    if selected_p_name:
        sel_p = next(p for p in filtered_progs if f"{p['country_vi']} - {p['program_name']}" == selected_p_name)
        chk = sel_p["checklist"]

        ct1, ct2, ct3, ct4, ct5 = st.tabs([
            "1. Nhân Thân & Hộ Tịch",
            "2. Năng Lực Tài Chính",
            "3. Chuyên Biệt Theo Diện",
            "4. Chỗ Ở & Y Tế",
            "5. Quy Chuẩn Nộp & HPHLS"
        ])

        with ct1:
            for it in chk["tier1_civil_identity"]:
                st.markdown(f"- **{it['item']}**: {it['detail']}")
        with ct2:
            for it in chk["tier2_financial_funds"]:
                st.markdown(f"- **{it['item']}**: {it['detail']}")
        with ct3:
            for it in chk["tier3_specialized_investment"]:
                st.markdown(f"- **{it['item']}**: {it['detail']}")
        with ct4:
            for it in chk["tier4_accommodation_health"]:
                st.markdown(f"- **{it['item']}**: {it['detail']}")
        with ct5:
            for it in chk["tier5_legalization_submission"]:
                st.markdown(f"- **{it['item']}**: {it['detail']}")


# ==============================================================================
# TAB 3: COUNTRY & PROGRAM EXPLORER (31 NƯỚC)
# ==============================================================================
with tab_explorer:
    st.markdown("### 🌍 Cơ Sở Dữ Liệu Chi Tiết 31 Quốc Gia EU & Schengen")
    st.caption("Khám phá từng quốc gia riêng biệt: Chỉ số di trú, chính sách 2025-2026, toàn bộ các diện visa và tải hồ sơ tài liệu quốc gia.")

    country_list = sorted(list(all_countries.keys()))
    country_display_map = {k: f"{all_countries[k]['country_vi']} ({all_countries[k]['country_en']})" for k in country_list}

    selected_country_slug = st.selectbox(
        "Chọn quốc gia cần tra cứu chi tiết:",
        options=country_list,
        format_func=lambda x: country_display_map[x]
    )

    c_data = all_countries[selected_country_slug]
    ov = c_data["overview"]
    diff = c_data.get("difficulty_and_stats", {})
    changes = c_data.get("recent_policy_changes", [])
    refs = c_data.get("official_references", [])
    progs = c_data["programs"]

    # Country Stat Header
    st.markdown(f"## 🏛️ {c_data['country_vi']} ({c_data['country_en']})")
    st.info(f"**Tình trạng:** {ov['eu_schengen_status']} | **Mức độ khó di trú:** {ov['difficulty_rating']} | **Website chính thức:** [{ov['official_portal']}](https://{ov['official_portal'].split('/')[0].strip()})")

    # Metrics Row
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Điểm MIPEX", f"{ov['mipex_score']}/100")
    with m2:
        st.metric("Tỷ Lệ Từ Chối Visa", f"{ov['visa_refusal_rate']}%")
    with m3:
        st.metric("Thời Gian Xử Lý", f"{diff.get('processing_months', '3-6')} tháng")
    with m4:
        st.metric("Lộ Trình PR", f"{diff.get('years_to_pr', '5')} năm")
    with m5:
        st.metric("Lộ Trình Quốc Tịch", f"{diff.get('years_to_citizenship', '10')} năm")

    # Policy Changes 2025-2026
    if changes:
        with st.expander("🔔 Cập Nhật Thay Đổi Chính Sách Di Trú 2025 - 2026", expanded=True):
            for ch in changes:
                st.markdown(f"- **[{ch.get('time', '')}] {ch.get('change', '')}**")
                st.markdown(f"  - *Tác động:* {ch.get('impact', '')}")
                st.markdown(f"  - *Trạng thái:* `{ch.get('status', '')}` | *Chi tiết:* {ch.get('detail', '')}")

    st.markdown("---")
    st.markdown(f"### 📋 Danh Sách {len(progs)} Chương Trình Định Cư Tại {c_data['country_vi']}")

    for p in progs:
        with st.expander(f"📌 {p['program_name']} ({p['archetype_name']})", expanded=False):
            st.markdown(f"- **Phân loại di trú:** `{p['category']}`")
            st.markdown(f"- **Yêu cầu tài chính:** {p['financial_requirement_text']}")
            st.markdown(f"- **Thời gian xử lý:** {p['processing_time']}")
            st.markdown(f"- **Thời gian đến Thường trú nhân (PR):** {p['timeline_pr']}")
            st.markdown(f"- **Thời gian đến Quốc tịch (Passport):** {p['timeline_citizenship']}")
            st.markdown(f"- **Yêu cầu cư trú thực tế:** Tối thiểu {p['min_physical_stay_days_per_year']} ngày/năm")
            st.markdown(f"- **Yêu cầu ngôn ngữ:** {p['language_requirement']}")
            st.markdown(f"- **Điều kiện tiên quyết:** {p['main_conditions']}")

            st.markdown("#### 📋 Bộ Checklist Hồ Sơ 5 Nhóm Chi Tiết")
            chk = p["checklist"]

            ch1, ch2, ch3, ch4, ch5 = st.tabs([
                "1. Nhân Thân & Hộ Tịch",
                "2. Năng Lực Tài Chính",
                "3. Chuyên Biệt Theo Diện",
                "4. Chỗ Ở & Y Tế",
                "5. Quy Chuẩn Nộp & HPHLS"
            ])

            with ch1:
                for it in chk["tier1_civil_identity"]:
                    st.markdown(f"- [ ] **{it['item']}**: {it['detail']}")
            with ch2:
                for it in chk["tier2_financial_funds"]:
                    st.markdown(f"- [ ] **{it['item']}**: {it['detail']}")
            with ch3:
                for it in chk["tier3_specialized_investment"]:
                    st.markdown(f"- [ ] **{it['item']}**: {it['detail']}")
            with ch4:
                for it in chk["tier4_accommodation_health"]:
                    st.markdown(f"- [ ] **{it['item']}**: {it['detail']}")
            with ch5:
                for it in chk["tier5_legalization_submission"]:
                    st.markdown(f"- [ ] **{it['item']}**: {it['detail']}")

    # Download Country Markdown Dossier
    country_md_file = os.path.join(COUNTRIES_DIR, f"{selected_country_slug}.md")
    if os.path.exists(country_md_file):
        with open(country_md_file, "r", encoding="utf-8") as f_md:
            md_content = f_md.read()
        st.download_button(
            f"📥 Tải Toàn Bộ Hồ Sơ Di Trú {c_data['country_vi']} (Markdown Dossier)",
            data=md_content,
            file_name=f"{selected_country_slug}_immigration_dossier.md",
            mime="text/markdown"
        )


# ==============================================================================
# TAB 4: SIDE-BY-SIDE PROGRAM COMPARISON
# ==============================================================================
with tab_compare:
    st.markdown("### ⚖️ So Sánh Song Song Các Chương Trình Định Cư (Side-by-Side Comparison)")
    st.caption("Chọn từ 2 đến 3 chương trình bất kỳ để đặt lên bàn cân so sánh chi phí, thời gian xử lý, nghĩa vụ cư trú và quyền lợi quốc tịch.")

    prog_display_options = [f"{p['country_vi']} - {p['program_name']} ({p['archetype_name']})" for p in all_programs]

    selected_comp_names = st.multiselect(
        "Chọn 2 hoặc 3 chương trình để so sánh:",
        options=prog_display_options,
        default=[
            prog_display_options[0],
            prog_display_options[1]
        ] if len(prog_display_options) >= 2 else []
    )

    if len(selected_comp_names) >= 2:
        selected_progs = []
        for name in selected_comp_names:
            p_obj = next(p for p in all_programs if f"{p['country_vi']} - {p['program_name']} ({p['archetype_name']})" == name)
            selected_progs.append(p_obj)

        comp_data = {
            "Tiêu Chí So Sánh": [
                "🏛️ Quốc Gia",
                "🏷️ Diện Định Cư / Visa",
                "📂 Phân Loại Archetype",
                "💶 Chi Phí / Vốn Yêu Cầu",
                "⏳ Thời Gian Xử Lý",
                "✈️ Nghĩa Vụ Cư Trú Thực Tế",
                "🛡️ Lộ Trình Thường Trú Nhân (PR)",
                "🛂 Lộ Trình Quốc Tịch (Passport)",
                "🗣️ Yêu Cầu Ngôn Ngữ",
                "👨‍👩‍👧‍👦 Chính Sách Gia Đình",
                "⚠️ Điều Kiện Cốt Lõi"
            ]
        }

        for p in selected_progs:
            col_key = f"{p['country_vi']}\n{p['program_name']}"
            comp_data[col_key] = [
                f"{p['country_vi']} ({p['country_en']})",
                p["program_name"],
                p["archetype_name"],
                p["financial_requirement_text"],
                p["processing_time"],
                f"Tối thiểu {p['min_physical_stay_days_per_year']} ngày/năm",
                p["timeline_pr"],
                p["timeline_citizenship"],
                p["language_requirement"],
                "Bảo lãnh vợ/chồng & con cái" + (" + Cha mẹ 2 bên" if p['country_slug'] in ['greece', 'malta', 'cyprus'] and p['archetype_id'] == 'golden_visa' else ""),
                p["main_conditions"]
            ]

        df_comp = pd.DataFrame(comp_data)
        st.table(df_comp)
    else:
        st.info("Vui lòng chọn ít nhất 2 chương trình ở mục trên để xem bảng so sánh song song.")


# ==============================================================================
# TAB 5: ARCHETYPES & MASTER CHECKLIST STANDARDS
# ==============================================================================
with tab_archetypes:
    st.markdown("### 📚 Khung Chuẩn Hóa 5 Diện Visa Di Trú Châu Âu & Bộ Checklist 5 Nhóm")
    st.caption("Khung tiêu chuẩn áp dụng thống nhất cho toàn bộ 31 quốc gia EU & Schengen.")

    arch_choice = st.selectbox(
        "Chọn diện visa để xem chuẩn mực quy định và danh mục hồ sơ:",
        options=list(archetypes_data.keys()),
        format_func=lambda x: f"{archetypes_data[x]['name_vi']} ({archetypes_data[x]['name_en']})"
    )

    arch_info = archetypes_data[arch_choice]

    st.markdown(f"### {arch_info['name_vi']}")
    st.markdown(f"> *{arch_info['description']}*")

    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        st.markdown(f"**Đối tượng hướng tới:**\n{arch_info['target_audience']}")
    with col_a2:
        st.markdown(f"**Khung tài chính:**\n`{arch_info['financial_range']}`")
    with col_a3:
        st.markdown(f"**Mức độ cư trú yêu cầu:**\n`{arch_info['physical_residency']}`")

    st.markdown("---")
    st.markdown("#### 📋 Tiêu Chuẩn 5 Nhóm Hồ Sơ Chi Tiết")

    chk = arch_info["checklist"]
    tier_titles = [
        ("Nhóm 1: Hồ Sơ Nhân Thân & Hộ Tịch (Civil & Identity Documents)", chk["tier1_civil_identity"]),
        ("Nhóm 2: Năng Lực Tài Chính & Nguồn Tiền Hợp Pháp (Financial & AML)", chk["tier2_financial_funds"]),
        ("Nhóm 3: Hồ Sơ Nghiệp Vụ Chuyên Biệt Theo Diện (Specialized Documents)", chk["tier3_specialized_investment"]),
        ("Nhóm 4: Chỗ Ở & Bảo Hiểm Y Tế Quốc Tế (Accommodation & Health)", chk["tier4_accommodation_health"]),
        ("Nhóm 5: Quy Chuẩn Nộp & Hợp Pháp Hóa Lãnh Sự (Legalization & Submission)", chk["tier5_legalization_submission"])
    ]

    for title, items in tier_titles:
        with st.expander(title, expanded=True):
            for item in items:
                st.markdown(f"- **{item['item']}**")
                st.markdown(f"  *{item['detail']}*")
