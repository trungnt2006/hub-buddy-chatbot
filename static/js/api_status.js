// Gọi GET /api/setup/status và chuẩn hoá lỗi mạng thành status bằng 0.
export async function apiStatus() {
  try {
    const res = await fetch("/api/setup/status", {
      method: "GET",
      headers: { Accept: "application/json" },
    });
    const duLieu = await res.json().catch(() => ({}));
    return { ok: res.ok, status: res.status, data: duLieu };
  } catch (loi) {
    return { ok: false, status: 0, data: { message: "Không kết nối được máy chủ" } };
  }
}
