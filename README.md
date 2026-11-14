# HỆ THỐNG KNOWLEDGE BASE & CÔNG CỤ MATCHING ĐỊNH CƯ CHÂU ÂU 2026
## EU & Schengen Immigration Analysis, Modular Knowledge Base & Smart Matching Engine

Dự án được xây dựng dựa trên cơ sở dữ liệu phân tích di trú Châu Âu 2025-2026 (`eu_schengen_immigration_analysis.xlsx`), bao gồm 31 quốc gia EU/Schengen và 79 chương trình định cư.

---

## 📁 CẤU TRÚC DỰ ÁN & DỮ LIỆU ĐÃ TÁCH

```
EU programs all types 2026/
├── data/
│   ├── countries/                          # 31 quốc gia được chia tách độc lập
│   │   ├── austria.json & austria.md
│   │   ├── belgium.json & belgium.md
│   │   ├── cyprus.json & cyprus.md
│   │   ├── germany.json & germany.md
│   │   ├── greece.json & greece.md
│   │   ├── hungary.json & hungary.md
│   │   ├── malta.json & malta.md
│   │   ├── portugal.json & portugal.md
│   │   ├── spain.json & spain.md
│   │   └── ... (đầy đủ 31 quốc gia)
│   ├── eu_immigration_master.json          # Master database 79 chương trình
│   └── archetypes_checklists.json          # Chuẩn hóa 5 diện visa & 5 nhóm checklist
├── scripts/
│   ├── standard_schemas.py                 # Định nghĩa 5 Archetype & Khung Checklist 5 nhóm
│   └── build_knowledge_base.py             # Script trích xuất & làm giàu dữ liệu từ Excel
├── matching_engine.py                      # Thuật toán tính điểm tương thích (Match Score %)
├── report_generator.py                     # Module tạo báo cáo tư vấn PDF & HTML Print-ready
├── app.py                                  # Ứng dụng Web tương tác Streamlit
├── run_app.sh                              # Lệnh khởi chạy nhanh ứng dụng
└── eu_schengen_immigration_analysis.xlsx   # File Excel gốc
```

---

## 🏛️ BỘ KHUNG CHUẨN HÓA 5 DIỆN VISA & CHECKLIST 5 NHÓM TIÊU CHUẨN

Mọi chương trình định cư của 31 quốc gia đều được ánh xạ về một trong 5 nhóm visa chủ lực:
1. **Đầu Tư & Golden Visa (`golden_visa`)**: Quỹ đầu tư, Bất động sản, Trái phiếu chính phủ.
2. **Lao Động Kỹ Năng Cao & EU Blue Card (`blue_card`)**: Chuyên gia, kỹ sư có bằng đại học và Job Offer.
3. **Du Mục Kỹ Thuật Số (`digital_nomad`)**: Làm việc từ xa cho công ty nước ngoài, Freelancer quốc tế.
4. **Thu Nhập Thụ Động / FIP (`passive_income`)**: Tiền cho thuê nhà, cổ tức, lương hưu, không đi làm công.
5. **Khởi Nghiệp & Doanh Nhân (`startup_entrepreneur`)**: Dự án sáng tạo, bảo trợ bởi Vườn ươm công nghệ.

### 5 Nhóm Hồ Sơ Chi Tiết Cho Mỗi Diện:
- **Nhóm 1: Nhân thân & Hộ tịch (Civil & Identity)**: Hộ chiếu, CCCD, Khai sinh, Kết hôn, Lý lịch Tư pháp số 2 (Apostille/HPHLS), Ảnh sinh trắc học.
- **Nhóm 2: Năng lực tài chính & Nguồn tiền (Financial & Clean Funds AML)**: Báo cáo kiểm toán nguồn tiền, Sao kê 6-12 tháng, Điện chuyển tiền SWIFT MT103, Mã số thuế & Tài khoản ngân hàng sở tại.
- **Nhóm 3: Hồ sơ nghiệp vụ chuyên biệt (Specialized Documents)**: Hợp đồng mua chứng chỉ quỹ CMVM/CSSF hoặc HĐ mua BĐS; HĐLĐ & Thẩm định văn bằng Anabin/ZAB; Hợp đồng làm việc từ xa & Tờ khai thuế; Business Plan & Thư bảo trợ Vườn ươm.
- **Nhóm 4: Chỗ ở & Bảo hiểm y tế (Accommodation & Health)**: Hợp đồng thuê nhà 12 tháng/Sổ đỏ; Bảo hiểm y tế quốc tế/nội địa toàn diện không đồng chi trả.
- **Nhóm 5: Quy chuẩn nộp & Hợp pháp hoá lãnh sự (Legalization & Submission)**: Giấy ủy quyền POA cho luật sư; Dịch thuật công chứng tư pháp; Lịch hẹn lăn tay tại cơ quan di trú.

---

## 🚀 HƯỚNG DẪN KHỞI CHẠY ỨNG DỤNG WEB (STREAMLIT APP)

Mở Terminal tại thư mục hiện tại và chạy một trong hai lệnh sau:

```bash
# Cách 1: Chạy file script bash
./run_app.sh

# Cách 2: Chạy trực tiếp qua Python
python3 -m streamlit run app.py
```

Ứng dụng sẽ tự động mở trên trình duyệt tại địa chỉ: `http://localhost:8501`.

### Các Tính Năng Chính Trên Ứng Dụng:
1. **🎯 Khảo Sát & Match Khách Hàng (Client Smart Wizard)**: Khách hàng nhập ngân sách, thu nhập, khả năng cư trú, học vấn, gia đình -> Hệ thống tự động tính điểm Match %, gợi ý Top chương trình tối ưu, hiển thị checklist và cho phép **Xuất Báo Cáo PDF / In ấn HTML**.
2. **⚡ Bộ Lọc Chuyên Viên (Advisor Quick Matrix)**: Bảng lọc tức thì 79 chương trình theo quốc gia, ngân sách, phân loại visa, yêu cầu cư trú và tải file CSV/Excel.
3. **🌍 Tra Cứu 31 Nước & Checklist**: Hồ sơ chi tiết từng quốc gia (Áo, Bỉ, Đức, Hy Lạp, Hungary, Malta, Bồ Đào Nha, Tây Ban Nha...), cập nhật chính sách 2025-2026 và tải Markdown Dossier.
4. **⚖️ So Sánh Song Song (Side-by-Side Comparison)**: Đặt 2-3 chương trình cạnh nhau để so sánh chi phí, thời gian xử lý, nghĩa vụ cư trú và quyền lợi quốc tịch.
5. **📚 Chuẩn Hóa 5 Diện Visa**: Cẩm nang chi tiết về 5 diện di trú chính của Châu Âu.
