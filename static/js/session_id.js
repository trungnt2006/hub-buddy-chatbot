// Sinh và giữ định danh phiên trong localStorage; không lưu khóa API ở đây.
let tam = null;
const HOP_LE = /^[A-Za-z0-9-]{8,64}$/;

function sinhId() {
  if (globalThis.crypto && typeof globalThis.crypto.randomUUID === "function") {
    return globalThis.crypto.randomUUID();
  }
  return "s-" + Math.random().toString(36).slice(2) + Date.now().toString(36);
}

export function getSessionId() {
  const khoa = "session_id";
  let gia = null;
  try {
    gia = localStorage.getItem(khoa);
  } catch (loi) {
    return tam || (tam = sinhId());
  }
  if (gia !== null && HOP_LE.test(gia)) {
    return gia;
  }
  const moi = sinhId();
  try {
    localStorage.setItem(khoa, moi);
  } catch (loi) {
    tam = moi;
  }
  return moi;
}
