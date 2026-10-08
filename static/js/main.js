// Điểm vào của trang: kiểm tra tài nguyên, hỏi trạng thái khóa rồi hiển thị.
import { apiStatus } from "./api_status.js";
import { setupDialog } from "./setup_dialog.js";
import { chatView } from "./chat_view.js";
import { getSessionId } from "./session_id.js";

function loiKhoiDong(tieuDe, dong) {
  const goc = document.getElementById("root");
  const khung = document.createElement("div");
  khung.setAttribute(
    "style",
    "max-width:600px;margin:80px auto;padding:32px;background:rgba(30,41,59,0.7);border-radius:16px;border:1px solid rgba(255,255,255,0.1);text-align:center;box-shadow:0 20px 40px rgba(0,0,0,0.5)"
  );
  const t = document.createElement("h2");
  t.setAttribute("style", "color:#f8fafc;margin-top:0;font-size:1.5rem");
  t.textContent = tieuDe;
  const p = document.createElement("p");
  p.setAttribute("style", "color:#cbd5e1;line-height:1.6");
  p.textContent = dong;
  const l = document.createElement("pre");
  l.setAttribute(
    "style",
    "background:#0f172a;color:#818cf8;padding:12px;border-radius:8px;font-size:0.9rem;overflow-x:auto"
  );
  l.textContent =
    "Start-Process powershell -ArgumentList '-NoExit','-Command','.\\run.bat'";
  const u = document.createElement("p");
  u.setAttribute("style", "color:#94a3b8;font-size:0.9rem");
  u.textContent = "Kiểm tra mạng rồi mở lại bằng http://127.0.0.1:2610.";
  const v = document.createElement("p");
  v.setAttribute("style", "color:#64748b;font-size:0.8rem");
  v.textContent =
    "URL CDN ghi UNVERIFIED cho tới khi thử: React 18, ReactDOM 18, MUI 5, phông Roboto, phông biểu tượng Material Symbols Outlined.";
  khung.append(t, p, l, u, v);
  goc.replaceChildren(khung);
}

function ve(node) {
  ReactDOM.createRoot(document.getElementById("root")).render(node);
}

export async function main() {
  const thieu =
    !globalThis.React || !globalThis.ReactDOM || !globalThis.MaterialUI;
  if (thieu) {
    loiKhoiDong(
      "Không tải được tài nguyên giao diện",
      "CDN không tải được, trình duyệt có thể đang chặn mạng."
    );
    return;
  }
  const trangThai = await apiStatus();
  if (!trangThai.ok) {
    const nhan =
      trangThai.status === 0
        ? "Không kết nối được máy chủ."
        : (trangThai.data && trangThai.data.message) || "Máy chủ trả lỗi.";
    loiKhoiDong("Chưa kết nối được chatbot", nhan);
    return;
  }
  const sessionId = getSessionId();
  const daCauHinh = Boolean(trangThai.data && trangThai.data.configured);
  ve(
    daCauHinh
      ? chatView(sessionId)
      : setupDialog(sessionId, () => ve(chatView(sessionId)))
  );
}

main();
