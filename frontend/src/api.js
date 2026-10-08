const HOP_LE = /^[A-Za-z0-9-]{8,64}$/;

export function getSessionId() {
  const k = "session_id";
  let s = null;
  try {
    s = localStorage.getItem(k);
  } catch (e) {
    // ignore
  }
  if (!s || !HOP_LE.test(s)) {
    s = (globalThis.crypto && typeof globalThis.crypto.randomUUID === "function")
      ? globalThis.crypto.randomUUID()
      : "ses-" + Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 8);
    try {
      localStorage.setItem(k, s);
    } catch (e) {
      // ignore
    }
  }
  return s;
}

export async function checkStatus() {
  try {
    const res = await fetch("/api/setup/status");
    const data = await res.json();
    return { ok: res.ok, data };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

export async function sendMessage(sessionId, message) {
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message }),
    });
    const data = await res.json();
    return { ok: res.ok, status: res.status, data };
  } catch (err) {
    return { ok: false, status: 0, data: { message: "Lỗi kết nối tới máy chủ." } };
  }
}

export async function resetChat(sessionId) {
  try {
    const res = await fetch("/api/reset", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId }),
    });
    const data = await res.json();
    return { ok: res.ok, data };
  } catch (err) {
    return { ok: false, data: { message: "Không thể kết nối máy chủ." } };
  }
}

export async function saveApiKey(apiKey, sessionId) {
  try {
    const res = await fetch("/api/setup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ api_key: apiKey, session_id: sessionId }),
    });
    const data = await res.json();
    return { ok: res.ok, data };
  } catch (err) {
    return { ok: false, data: { message: "Không thể lưu khóa API." } };
  }
}
