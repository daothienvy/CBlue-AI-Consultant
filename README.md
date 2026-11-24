# CBLUE IMMIGRATION CONSULTANT — EU & SCHENGEN IMMIGRATION MATCHING TOOL 2026
## Ứng Dụng Web / Mobile App (PWA) Triển Khai Trên Vercel & Streamlit Cloud

Hệ thống tư vấn và đánh giá hồ sơ định cư Châu Âu chuyên sâu dành cho khách hàng và chuyên viên di trú của **CBlue Immigration**, dựa trên cơ sở dữ liệu Luật Di Trú Châu Âu cập nhật 2025-2026.

* 📞 **Hotline & Zalo:** **`0941 906 868`** (Link chat Zalo: [https://zalo.me/0941906868](https://zalo.me/0941906868))
* ✉️ **Email:** **`daothienvy25@gmail.com`**
* 🔗 **GitHub Repository:** [https://github.com/daothienvy/CBlue-AI-Consultant.git](https://github.com/daothienvy/CBlue-AI-Consultant.git)

---

## ⚡ HƯỚNG DẪN 3 BƯỚC DEPLOY LÊN VERCEL (https://vercel.com)

Vercel là nền tảng điện toán đám mây serverless hàng đầu thế giới, mang lại tốc độ tải trang gần như tức thì (<0.1 giây), hỗ trợ HTTPS tự động, băng thông toàn cầu và miễn phí 100%.

### Các bước thực hiện:
1. **Bước 1: Đăng nhập Vercel**
   * Truy cập: [https://vercel.com](https://vercel.com)
   * Bấm **"Log in"** hoặc **"Sign Up"** $\rightarrow$ Chọn **"Continue with GitHub"** (đăng nhập bằng tài khoản GitHub `daothienvy`).
2. **Bước 2: Import Dự Án**
   * Tại Dashboard Vercel, bấm nút **"Add New..."** ở góc phải trên $\rightarrow$ Chọn **"Project"**.
   * Trong danh sách GitHub Repositories, tìm repo **`CBlue-AI-Consultant`** và bấm **"Import"**.
3. **Bước 3: Bấm Deploy (Không cần cấu hình gì thêm)**
   * Vercel sẽ tự động đọc file `vercel.json` và nhận diện giao diện Web App tĩnh (`index.html`) cùng các Serverless Python API (`/api/`).
   * Bạn có thể sửa ô **Project Name** thành: `cblue-ai-consultant` (hoặc tên tùy chọn).
   * Bấm nút **"Deploy"**!
   * Sau khoảng **10 - 20 giây**, Vercel sẽ báo thành công và cấp cho bạn đường link công khai dạng:
     👉 **`https://cblue-ai-consultant.vercel.app`**

---

## 📱 CÁCH KHÁCH HÀNG CÀI ĐẶT NHƯ APP TRÊN ĐIỆN THOẠI (PWA)

Khách hàng **không cần phải lên App Store hay Google Play**, chỉ cần 2 thao tác khi mở link trên điện thoại:

* **Trên iPhone (Trình duyệt Safari):**
  1. Mở link web trên Safari.
  2. Bấm vào nút **Chia sẻ** (biểu tượng hình vuông có mũi tên lên ⬆️ ở thanh dưới cùng).
  3. Chọn **"Thêm vào Màn hình chính" (Add to Home Screen)** $\rightarrow$ Bấm **"Thêm"**.
  4. Biểu tượng ứng dụng **CBlue AI** sẽ xuất hiện ngay trên màn hình chính của iPhone như một App thông thường!
* **Trên Android (Trình duyệt Google Chrome):**
  1. Mở link web trên Chrome.
  2. Bấm vào biểu tượng **3 dấu chấm ⋮** ở góc phải trên.
  3. Chọn **"Cài đặt ứng dụng"** hoặc **"Thêm vào Màn hình chính"**.
  4. Ứng dụng sẽ được cài đặt và mở mượt mà toàn màn hình không có thanh địa chỉ web!

---

## 🏛️ CÁC TÍNH NĂNG CHÍNH CỦA ỨNG DỤNG VERCEL WEB / APP

1. **🎯 Khảo Sát & Match Khách Hàng (Smart Intake Quiz):**
   * Khách hàng điền thông tin liên hệ (Họ tên, SĐT/Zalo, Email) và nhu cầu ngân sách, thu nhập, khả năng cư trú.
   * Thuật toán chạy tức thì trong 0 giây, tính điểm tương thích (Match Score %) với 79 chương trình định cư.
   * Hiển thị Top 3 chương trình tối ưu kèm ưu điểm (Pros), lưu ý (Caveats) và bộ checklist hồ sơ 5 nhóm.
   * Nút hành động trực tiếp: **💬 Nhắn Tin Zalo**, **📞 Gọi Hotline**, **✉️ Gửi Email** và **🖨️ In Báo Cáo / Lưu PDF**.
2. **⚡ Bộ Lọc Chuyên Viên (Advisor Quick Matrix):**
   * Ma trận lọc thời gian thực 79 chương trình theo quốc gia, mức đầu tư, diện visa, nghĩa vụ cư trú.
   * Nút tải bảng dữ liệu ra file Excel/CSV.
   * Bấm vào bất kỳ chương trình nào để mở popup xem trọn bộ Checklist hồ sơ 5 nhóm.
3. **🌍 Tra Cứu 31 Nước EU & Checklist Hồ Sơ 5 Nhóm:**
   * Hồ sơ di trú chi tiết từng nước, chỉ số MIPEX, tỷ lệ từ chối visa, cập nhật chính sách 2025-2026.
4. **⚖️ So Sánh Song Song (Side-by-Side Comparison):**
   * Đặt 2-3 chương trình cạnh nhau so sánh chi phí, thời gian xử lý, nghĩa vụ cư trú và quyền lợi quốc tịch.
5. **📇 Quản Lý Khách Hàng (Leads CRM):**
   * Tự động lưu trữ danh sách khách hàng đã hoàn thành khảo sát (Lưu trữ trên trình duyệt + đồng bộ qua `/api/lead`).
   * Xuất danh sách khách hàng ra file Excel / CSV để chuyên viên chăm sóc.

---

## 💻 CHẠY LOCAL TRÊN MÁY TÍNH

* **Chạy bản Vercel Web App:**
  ```bash
  python3 -m http.server 3000
  # Mở trình duyệt tại: http://localhost:3000
  ```
* **Chạy bản Streamlit App:**
  ```bash
  python3 -m streamlit run app.py
  # Mở trình duyệt tại: http://localhost:8501
  ```
