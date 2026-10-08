# AGENTS.md - chatbot web, blueprint v4

## 1. Thứ tự đọc 10 prompt

- Đọc đúng thứ tự: P0, P1, P2, P3, P4, P5, P6, P7, P8, P9.
- Không bỏ P0. Không viết P7 trước P6.

## 2. Bảy luật bắt buộc

L1 KISS: giải pháp đơn giản nhất là giải pháp đúng; chỉ thêm tính năng khi có test.

L2 DDD: interface -> application -> domain; infrastructure -> domain. domain không import flask, langchain, openai, dotenv, os, pathlib, json, không mở tệp.

L3 TDD: viết test trước, chạy thấy ĐỎ, viết lượng mã nhỏ nhất làm XANH, rồi dọn.

L4 Mỗi hàm hoặc mỗi lớp một tệp; mỗi tệp dưới 100 dòng, kể cả tệp test và tệp js.

L5 Cấu hình và khóa API chỉ nằm trong tệp .env; không ghi cứng trong mã, không ghi cứng tên biến.

L6 An toàn: không ghi khóa API vào log, bộ nhớ, phản hồi hay thông điệp lỗi; hiển thị bằng chuỗi con của React; chỉ chấp nhận 127.0.0.1 và localhost.

L7 Windows 11, chỉ PowerShell; gọi Python bằng py; máy chủ chạy bằng Start-Process.

## 3. Danh sách tệp được phép tạo

- gốc: AGENTS.md, .env, .env.example, .gitignore, requirements.txt, pytest.ini, run.py, system-prompt.txt, memory.json
- src/chatbot/: __init__.py, config/, domain/, application/, infrastructure/, interface/
- config/: settings.py, load_settings.py, settings_error.py
- domain/: message.py, trim_history.py, errors.py, ports/memory_repository.py, ports/chat_model.py, ports/api_key_store.py
- application/: send_message.py, reset_conversation.py, configure_api_key.py, get_setup_status.py, validate_session_id.py, validate_message.py, validate_api_key.py
- infrastructure/: atomic_write_json.py, json_memory_repository.py, langchain_chat_model.py, load_system_prompt.py, env_api_key_store.py, atomic_write_text.py, map_openai_error.py, mask_secret.py
- interface/: create_app.py, json_error.py, require_json.py, require_localhost.py, routes/health_route.py, routes/setup_status_route.py, routes/setup_route.py, routes/chat_route.py, routes/reset_route.py
- static/: index.html, js/session_id.js, js/api_status.js, js/api_setup.js, js/api_chat.js, js/api_reset.js, js/message_bubble.js, js/setup_dialog.js, js/chat_view.js, js/send_handler.js, js/main.js
- tests/: test_load_settings.py, test_trim_history.py, test_validators.py, test_send_message.py, test_reset_conversation.py, test_configure_api_key.py, test_atomic_write.py, test_json_memory_repository.py, test_env_api_key_store.py, test_langchain_chat_model.py, test_map_openai_error.py, test_load_system_prompt.py, test_routes.py, test_first_run_flow.py, test_domain_purity.py, test_static_rules.py, fakes/fake_memory_repository.py, fakes/fake_chat_model.py, fakes/fake_api_key_store.py

## 4. Luồng khóa API lần đầu

1. py run.py khởi động server tại http://127.0.0.1:2610 khi CHƯA có khóa; không được sập.
2. Trang gọi GET /api/setup/status.
3. {"configured": false} hiện hộp thoại MUI "Nhập khóa API" gồm ô mật khẩu và nút Lưu.
4. Học viên dán khóa, bấm Lưu => POST /api/setup với {"api_key": "<khóa>"}.
5. Server kiểm hình thức khóa, ghi nguyên tử dòng OPENAI_API_KEY= vào .env, cập nhật bộ nhớ tiến trình, trả {"ok": true}.
6. Trang đóng hộp thoại, hiện khung chat; chat chạy ngay, không khởi động lại.
7. Lần sau status trả {"configured": true} => vào thẳng khung chat.
8. Khóa chỉ nằm trong .env; không vào log, không vào memory.json, không vào phản hồi.

## 5. Luật hành xử của opencode

- KHÔNG hỏi học viên khóa API trong cuộc hội thoại này.
- KHÔNG nhận khóa API dán từ học viên; chatbot tự hỏi khóa trên trang.
- Học viên dán khóa vào chat: từ chối, nhắc mở http://127.0.0.1:2610 và nhập ở hộp thoại.
- AGENTS.md đã tồn tại: hỏi trước khi ghi đè; chỉ ghi đè khi được xác nhận.
- Bản thảo AGENTS.md vượt 100 dòng: cắt xuống dưới 100 dòng trước khi báo xong.
- Không tạo tệp ngoài danh sách mục 3; cần tệp mới thì sửa mục 3 trước.
- Không dùng innerHTML hay dangerouslySetInnerHTML.
- Sau mỗi thay đổi: chạy py -m pytest -q rồi báo số test xanh.

## 6. Kiểm chứng nhanh

- rg "L1|L2|L3|L4|L5|L6|L7" AGENTS.md => 7 luật.
- (Get-Content AGENTS.md | Measure-Object -Line).Lines => nhỏ hơn 100.
- rg "sk" -g "!.venv" . => không dòng nào chứa khóa thật.
