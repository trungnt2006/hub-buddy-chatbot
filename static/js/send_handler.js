// Gửi một lượt chat và trả về trạng thái mới cho khung chat.
import { apiChat } from "./api_chat.js";

export async function sendHandler(trangThai, text) {
  const hienTai = trangThai.history.concat([{ role: "human", content: text }]);
  const kq = await apiChat(trangThai.sessionId, text);
  if (kq.ok) {
    const traLoi = (kq.data && kq.data.reply) || "";
    return {
      history: hienTai.concat([{ role: "ai", content: traLoi }]),
      error: "",
      canSetup: false,
      setupMessage: "",
    };
  }
  if (kq.status === 409) {
    return {
      history: hienTai,
      error: "",
      canSetup: true,
      setupMessage: "Chưa có khóa API, hãy nhập lại.",
    };
  }
  if (kq.status === 401 || kq.status === 402) {
    return {
      history: hienTai,
      error: (kq.data && kq.data.message) || "",
      canSetup: true,
      setupMessage: (kq.data && kq.data.message) || "Khóa API không đúng hoặc hết hạn mức.",
    };
  }
  const nhan = (kq.data && kq.data.message) || "";
  const gh =
    kq.status === 0
      ? "Không kết nối được máy chủ."
      : nhan || "Lỗi máy chủ, thử lại.";
  return { history: hienTai, error: gh, canSetup: false, setupMessage: "" };
}
