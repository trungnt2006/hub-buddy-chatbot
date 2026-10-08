// Gửi tin nhắn tới POST /api/chat; thân chỉ có message và session_id.
export async function apiChat(sessionId, message) {
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ message: message, session_id: sessionId }),
    });
    const duLieu = await res.json().catch(() => ({}));
    return { ok: res.ok, status: res.status, data: duLieu };
  } catch (loi) {
    return { ok: false, status: 0, data: { message: "Không kết nối được máy chủ" } };
  }
}
