// Gửi khóa API tới POST /api/setup; không ghi khóa vào bộ nhớ trình duyệt.
export async function apiSetup(apiKey) {
  try {
    const res = await fetch("/api/setup", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ api_key: apiKey }),
    });
    const duLieu = await res.json().catch(() => ({}));
    return { ok: res.ok, status: res.status, data: duLieu };
  } catch (loi) {
    return { ok: false, status: 0, data: { message: "Không kết nối được máy chủ" } };
  }
}
