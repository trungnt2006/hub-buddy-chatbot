import { messageBubble } from "./message_bubble.js";
import { sendHandler } from "./send_handler.js";
import { apiReset } from "./api_reset.js";
import { setupDialog } from "./setup_dialog.js";
import { IconArrowUp, IconReset } from "./icons.js";

const GOI_Y = [
  "Lên lịch ôn thi tuần này",
  "Kỹ thuật học Pomodoro & Feynman",
  "Tóm tắt bài học trọng tâm"
];

function Khung(props) {
  const [lichSu, setLichSu] = React.useState([]);
  const [text, setText] = React.useState("");
  const [cho, setCho] = React.useState(false);
  const [loi, setLoi] = React.useState("");
  const [moKhoa, setMoKhoa] = React.useState(null);
  const vung = React.useRef(null);

  React.useEffect(() => { if (vung.current) vung.current.scrollTop = vung.current.scrollHeight; }, [lichSu, cho]);

  const gui = async (nd) => {
    const ban = (typeof nd === "string" ? nd : text).trim();
    if (!ban || cho) return;
    setCho(true); setLoi(""); setText("");
    const kq = await sendHandler({ sessionId: props.sessionId, history: lichSu }, ban);
    setLichSu(kq.history); setCho(false); setLoi(kq.error);
    setMoKhoa(kq.canSetup ? kq.setupMessage : null);
  };

  const moi = async () => {
    const kq = await apiReset(props.sessionId);
    if (kq.ok) { setLichSu([]); setLoi(""); } else setLoi((kq.data && kq.data.message) || "Không xóa được lịch sử.");
  };

  const nhanPhim = (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); gui(); } };

  const emptyState = lichSu.length === 0 ? React.createElement(
    MaterialUI.Box, { sx: { my: "auto", py: 6, textAlign: "left", maxWidth: 640, mx: "auto", width: "100%" } },
    React.createElement(MaterialUI.Typography, { variant: "h4", fontWeight: 700, color: "#f8fafc", mb: 1, letterSpacing: "-0.02em" }, "HUB-Buddy"),
    React.createElement(MaterialUI.Typography, { variant: "body1", color: "#94a3b8", mb: 4 }, "Trợ lý AI đồng hành giải đề, tóm tắt và ôn thi cùng bạn."),
    React.createElement(MaterialUI.Typography, { variant: "caption", color: "#64748b", fontWeight: 600, display: "block", mb: 1.5, textTransform: "uppercase", letterSpacing: "0.05em" }, "Thử hỏi"),
    React.createElement(MaterialUI.Box, { sx: { display: "flex", flexDirection: "column", gap: 1 } },
      GOI_Y.map((q, i) => React.createElement(MaterialUI.Box, { key: i, onClick: () => gui(q), sx: { p: "12px 16px", bgcolor: "#18181b", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "14px", cursor: "pointer", color: "#e2e8f0", fontSize: "0.92rem", transition: "all 0.15s", "&:hover": { bgcolor: "#27272a", borderColor: "rgba(255,255,255,0.16)", transform: "translateX(4px)" } } }, q))
    )
  ) : null;

  return React.createElement(
    MaterialUI.Box, { sx: { width: "100%", height: "100vh", display: "flex", flexDirection: "column", bgcolor: "#090d16" } },
    React.createElement(MaterialUI.Box, { sx: { height: 56, borderBottom: "1px solid rgba(255,255,255,0.08)", bgcolor: "rgba(9,13,22,0.9)", backdropFilter: "blur(12px)", display: "flex", alignItems: "center", px: 3, flexShrink: 0 } },
      React.createElement(MaterialUI.Box, { sx: { maxWidth: 768, width: "100%", mx: "auto", display: "flex", alignItems: "center", justifyContent: "space-between" } },
        React.createElement(MaterialUI.Box, { sx: { display: "flex", alignItems: "center", gap: 1.2 } },
          React.createElement(MaterialUI.Typography, { variant: "subtitle1", fontWeight: 700, color: "#fff" }, "HUB-Buddy"),
          React.createElement(MaterialUI.Box, { sx: { display: "flex", alignItems: "center", gap: 0.6, bgcolor: "rgba(255,255,255,0.05)", px: 1, py: 0.3, borderRadius: "99px" } },
            React.createElement("span", { className: "pulse-dot" }),
            React.createElement(MaterialUI.Typography, { variant: "caption", color: "#94a3b8", fontSize: "0.75rem" }, "OpenCode · space-bunny-free")
          )
        ),
        React.createElement(MaterialUI.Button, { onClick: moi, size: "small", sx: { color: "#94a3b8", textTransform: "none", fontSize: "0.85rem", gap: 0.8, borderRadius: "10px", "&:hover": { color: "#f8fafc", bgcolor: "rgba(255,255,255,0.06)" } } },
          IconReset(16, "currentColor"), "Đoạn chat mới"
        )
      )
    ),
    React.createElement(MaterialUI.Box, { ref: vung, sx: { flex: 1, overflowY: "auto", px: 2, py: 2 } },
      React.createElement(MaterialUI.Box, { sx: { maxWidth: 768, width: "100%", mx: "auto", minHeight: "100%", display: "flex", flexDirection: "column" } },
        loi ? React.createElement(MaterialUI.Alert, { severity: "error", sx: { mb: 2, borderRadius: "12px" } }, loi) : null,
        emptyState, lichSu.map((m, i) => messageBubble(m.role, m.content, i)),
        cho ? React.createElement(MaterialUI.Box, { className: "fade-in", sx: { display: "flex", alignItems: "center", gap: 1.5, py: 2, color: "#94a3b8" } }, React.createElement("span", { className: "pulse-dot" }), React.createElement(MaterialUI.Typography, { variant: "body2", fontSize: "0.95rem" }, "HUB-Buddy đang soạn câu trả lời...")) : null
      )
    ),
    React.createElement(MaterialUI.Box, { sx: { px: 2, pb: 2, pt: 1, flexShrink: 0 } },
      React.createElement(MaterialUI.Box, { sx: { maxWidth: 768, width: "100%", mx: "auto" } },
        React.createElement(MaterialUI.Box, { sx: { display: "flex", alignItems: "flex-end", gap: 1, bgcolor: "#18181b", p: "8px 10px 8px 16px", borderRadius: "24px", border: "1px solid rgba(255,255,255,0.12)", transition: "border 0.2s", "&:focus-within": { borderColor: "#6366f1", boxShadow: "0 0 0 1px #6366f1" } } },
          React.createElement(MaterialUI.TextField, { fullWidth: true, multiline: true, maxRows: 6, value: text, disabled: cho, placeholder: "Hỏi về môn học, bài tập hoặc ôn thi...", onChange: (e) => setText(e.target.value), onKeyDown: nhanPhim, variant: "standard", InputProps: { disableUnderline: true, sx: { color: "#f8fafc", fontSize: "0.95rem", py: 0.5 } } }),
          React.createElement(MaterialUI.Button, { variant: "contained", disabled: cho || !text.trim(), onClick: () => gui(), sx: { minWidth: 38, width: 38, height: 38, borderRadius: "16px", p: 0, bgcolor: "#6366f1", color: "#fff", boxShadow: "none", "&:hover": { bgcolor: "#4f46e5" }, "&:disabled": { opacity: 0.3, bgcolor: "#3f3f46", color: "#71717a" } }, "aria-label": "Gửi tin" }, IconArrowUp(18, "#ffffff"))
        ),
        React.createElement(MaterialUI.Typography, { variant: "caption", color: "#52525b", display: "block", textAlign: "center", mt: 1, fontSize: "0.75rem" }, "Nhấn Enter để gửi • Shift + Enter để xuống dòng")
      )
    ),
    moKhoa ? React.createElement(setupDialog, { sessionId: props.sessionId, onDone: () => setMoKhoa(null), thongBao: moKhoa }) : null
  );
}

export function chatView(sessionId) { return React.createElement(Khung, { sessionId }); }



