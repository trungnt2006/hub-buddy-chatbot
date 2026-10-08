# 🎓 HUB-Buddy — Trợ lý Học Tập AI

> **Cố vấn trí tuệ nhân tạo chuyên sâu hỗ trợ giải đề, lên lịch ôn thi và phương pháp học tập tối ưu cho sinh viên HUB.**

---

## 🌟 Tính Năng Nổi Bật

- 🤖 **Trợ lý AI Đa Nhiệm:** Hỗ trợ giải bài tập, tóm tắt bài giảng, phân tích luận điểm cốt lõi và định lý quan trọng.
- 📅 **Lên Lịch Ôn Thi Tự Động:** Gợi ý lộ trình ôn tập phân bổ khoa học theo môn thi và điểm rơi phong độ.
- 🧠 **Phương Pháp Học Hiện Đại:** Tích hợp kỹ thuật **Pomodoro** (chu kỳ tập trung ngắt quãng) và **Feynman** (giải thích đơn giản hóa để hiểu sâu).
- ⚡ **Giao Diện Studio Hiện Đại:** Thiết kế Dark Mode tối giản, trung tính cao cấp (chuẩn ChatGPT / Linear), thanh bên gập mở mượt mà và các thẻ tác vụ nhanh.
- 🔑 **Linh Hoạt API:** Hỗ trợ mô hình OpenCode AI (`space-bunny-free`) tốc độ cao cùng chế độ dự phòng OpenAI tiêu chuẩn.

---

## 🛠️ Công Nghệ Sử Dụng

### Backend
- **Python 3.12+** & **Flask**
- **Kiến trúc Domain-Driven Design (DDD):** Tách bạch Domain, Application, Infrastructure và Interface.
- **LangChain Core & Community**
- **Pytest:** Đạt 100% test coverage với 177 unit & integration tests.

### Frontend
- **Vite** & **React 18**
- **Tailwind CSS v4**
- **Lucide React Icons**

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Ứng Dụng

### 1. Khởi động nhanh trên Windows
Chỉ cần nhấp đúp vào tệp:
```cmd
run.bat
```
Tệp sẽ tự động kích hoạt môi trường Python ảo và mở trình duyệt tại:
👉 `http://127.0.0.1:2610`

### 2. Chạy thủ công bằng Terminal

```bash
# 1. Kích hoạt môi trường ảo
.\.venv\Scripts\activate

# 2. Cài đặt các gói phụ thuộc (nếu lần đầu)
pip install -r requirements.txt

# 3. Khởi chạy máy chủ
python run.py
```

### 3. Phát triển Frontend với Hot-Reload (Tùy chọn)

Nếu bạn muốn tùy biến giao diện trực tiếp với tính năng HMR của Vite:
```bash
cd frontend
npm install
npm run dev
```
Trình duyệt sẽ mở tại `http://localhost:5173` và tự động proxy các lệnh gọi `/api` về máy chủ Flask.

---

## 🔒 Bảo Mật & Cấu Hình

Tạo tệp `.env` tại thư mục gốc từ bản mẫu:
```bash
cp .env.example .env
```
Cấu hình các tham số:
```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=space-bunny-free
OPENAI_BASE_URL=https://opencode.ai/zen/v1
PORT=2610
HOST=127.0.0.1
```
*(Khóa API được lưu cục bộ an toàn trên máy bạn, không bao giờ gửi ra bên ngoài ngoại trừ endpoint mô hình đã định cấu hình).*

---

## 🧪 Kiểm Thử

Chạy toàn bộ bộ kiểm thử tự động:
```bash
pytest
```

---

## 📄 Bản Quyền
Dự án được phát triển phục vụ mục đích học tập và nghiên cứu.
