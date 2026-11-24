# CBLUE IMMIGRATION CONSULTANT — EU & SCHENGEN IMMIGRATION MATCHING TOOL 2026
## Hệ Thống Knowledge Base 31 Quốc Gia, Thuật Toán Matching Đa Chiều & Quản Lý Leads Khách Hàng

Ứng dụng tư vấn định cư chuyên sâu dành cho khách hàng và chuyên viên di trú của **CBlue Immigration**, dựa trên cơ sở dữ liệu Luật Di Trú Châu Âu cập nhật 2025-2026.

---

## 🚀 HƯỚNG DẪN TRIỂN KHAI LÊN STREAMLIT COMMUNITY CLOUD (MIỄN PHÍ)

Chỉ với 4 bước đơn giản, bạn có ngay đường link web HTTPS công khai để gửi cho khách hàng:

1. **Truy cập:** [https://share.streamlit.io](https://share.streamlit.io) và đăng nhập bằng tài khoản GitHub `daothienvy`.
2. **Tạo App Mới:** Bấm vào nút **"Create app"** (hoặc **"New app"**).
3. **Cấu hình thông số:**
   * **Repository:** `daothienvy/CBlue-AI-Consultant`
   * **Branch:** `main`
   * **Main file path:** `app.py`
   * **App URL (tùy chọn):** Bạn có thể gõ `cblue-consultant` để có link đẹp dạng `https://cblue-consultant.streamlit.app`.
4. **Bấm "Deploy!":** Hệ thống sẽ tự động cài đặt các thư viện trong `requirements.txt` và khởi chạy trong vòng 60-90 giây.

Sau khi deploy thành công, bạn có thể copy đường link này gửi qua Zalo, Facebook, gắn vào Bio hoặc nhúng vào Website của CBlue!

---

## 📱 HƯỚNG DẪN CÀI ĐẶT NHƯ APP TRÊN ĐIỆN THOẠI (PWA)

Khách hàng không cần lên App Store hay Google Play, chỉ cần mở link web và thực hiện 2 thao tác:
* **Trên iPhone (Safari):** Bấm nút **Chia sẻ (Share ⬆️)** ở thanh dưới cùng $\rightarrow$ Chọn **"Thêm vào Màn hình chính" (Add to Home Screen)** $\rightarrow$ Bấm **"Thêm"**.
* **Trên Android (Chrome):** Bấm vào biểu tượng **3 dấu chấm ⋮** ở góc phải $\rightarrow$ Chọn **"Cài đặt ứng dụng"** hoặc **"Thêm vào Màn hình chính"**.

Biểu tượng ứng dụng CBlue sẽ xuất hiện trên màn hình điện thoại của khách hàng như một App native!

---

## 🏛️ CÁC TÍNH NĂNG CHÍNH CỦA HỆ THỐNG

1. **🎯 Khảo Sát & Match Khách Hàng (Client Smart Wizard):**
   * Thu thập thông tin liên hệ (Họ tên, SĐT/Zalo, Email) và nhu cầu tài chính, cư trú.
   * Chấm điểm tương thích (Match Score 0-100%) với 79 chương trình định cư.
   * Nút kết nối nhanh: **💬 Nhắn Tin Zalo** và **📞 Gọi Hotline**.
   * Xuất **Báo Cáo PDF Chuẩn CBlue** và **Bản In Báo Cáo HTML Print-Ready**.
2. **⚡ Bộ Lọc Chuyên Viên (Advisor Quick Matrix):**
   * Ma trận lọc thời gian thực 79 chương trình theo quốc gia, mức đầu tư, nghĩa vụ cư trú.
   * Xuất file CSV/Excel cho chuyên viên.
3. **🌍 Tra Cứu 31 Nước & Checklist Hồ Sơ 5 Nhóm:**
   * Hồ sơ di trú chi tiết từng nước, chỉ số MIPEX, cập nhật chính sách 2025-2026.
   * Tải hồ sơ Markdown Dossier cho từng quốc gia.
4. **⚖️ So Sánh Song Song (Side-by-Side):**
   * Đặt 2-3 chương trình cạnh nhau so sánh chi phí, thời gian xử lý, nghĩa vụ cư trú và quyền lợi quốc tịch.
5. **📚 Khung Chuẩn Hóa 5 Diện Visa:**
   * Cẩm nang chuẩn mực về Đầu tư & Golden Visa, EU Blue Card, Digital Nomad, Thu nhập thụ động FIP, Startup.
6. **📇 Quản Lý Khách Hàng (Leads CRM):**
   * Tự động lưu trữ danh sách khách hàng đã hoàn thành khảo sát.
   * Hiển thị họ tên, số điện thoại, ngân sách, chương trình quan tâm và xuất file Excel chăm sóc khách hàng.

---

## 💻 CHẠY ỨNG DỤNG LOCAL TRÊN MÁY TÍNH

```bash
# Cách 1: Chạy file script
./run_app.sh

# Cách 2: Chạy trực tiếp qua Python
python3 -m streamlit run app.py
```
Ứng dụng sẽ mở tại: `http://localhost:8501`.
