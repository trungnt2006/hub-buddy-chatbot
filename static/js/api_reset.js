// Gọi POST /api/reset để xóa lịch sử máy chủ cho một phiên.
export async function apiReset(sessionId) {
  try {
    const res = await fetch("/api/reset", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ session_id: sessionId }),
    });
    const duLieu = await res.json().catch(() => ({}));
    return { ok: res.ok, status: res.status, data: duLieu };
  } catch (loi) {
    return { ok: false, status: 0, data: { message: "Không kết nối được máy chủ" } };
  }
}
