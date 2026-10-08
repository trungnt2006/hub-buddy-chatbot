import { apiSetup } from "./api_setup.js";
import { IconKey } from "./icons.js";

function NoiDungHopThoai(props) {
  const [gia, setGia] = React.useState("");
  const [dangGui, setDangGui] = React.useState(false);
  const [loi, setLoi] = React.useState(props.thongBao || "");

  const gui = async () => {
    if (dangGui) return;
    setDangGui(true); setLoi("");
    const kq = await apiSetup(gia);
    setGia(""); setDangGui(false);
    if (kq.ok) { props.onDone(true, ""); return; }
    const nhan = (kq.data && kq.data.message) || "";
    if (kq.status === 0) setLoi("Không kết nối được máy chủ, hãy chạy run.bat.");
    else if (kq.status === 403) setLoi("Chỉ được truy cập bằng http://127.0.0.1:2610.");
    else setLoi(nhan || "Không lưu được khóa API, hãy thử lại.");
  };

  const nhanPhim = (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); gui(); } };

  return React.createElement(
    MaterialUI.Dialog, {
      open: true, fullWidth: true, maxWidth: "sm", "aria-label": "Hộp thoại nhập khóa API",
      PaperProps: { sx: { bgcolor: "#0f172a", color: "#f8fafc", border: "1px solid rgba(255,255,255,0.12)", borderRadius: "16px", p: 1.5, boxShadow: "0 25px 60px rgba(0,0,0,0.8)" } },
    },
    React.createElement(MaterialUI.DialogTitle, null,
      React.createElement(MaterialUI.Box, { sx: { display: "flex", alignItems: "center", gap: 1.5 } },
        React.createElement(MaterialUI.Box, { sx: { width: 36, height: 36, borderRadius: "10px", display: "flex", alignItems: "center", justifyContent: "center", background: "linear-gradient(135deg, #6366f1, #3b82f6)", color: "#fff" } },
          IconKey(20, "#ffffff")
        ),
        React.createElement(MaterialUI.Typography, { variant: "h6", fontWeight: 700, color: "#fff" }, "Cấu hình khóa API")
      )
    ),
    React.createElement(MaterialUI.DialogContent, null,
      loi ? React.createElement(MaterialUI.Alert, { severity: "error", sx: { mb: 2, borderRadius: "10px" } }, loi) : null,
      React.createElement(MaterialUI.Typography, { variant: "body2", color: "#94a3b8", mb: 2 }, "Nhập API key (OpenAI hoặc OpenCode). Khóa chỉ lưu cục bộ tại tệp .env trên máy của bạn."),
      React.createElement(MaterialUI.TextField, {
        autoFocus: true, fullWidth: true, type: "password", label: "Khóa API", value: gia,
        onChange: (e) => setGia(e.target.value), onKeyDown: nhanPhim, disabled: dangGui,
        inputProps: { maxLength: 200, "aria-label": "Ô nhập khóa API" },
        helperText: "An toàn tuyệt đối — không lưu vào trình duyệt.",
        sx: { "& .MuiOutlinedInput-root": { color: "#f8fafc", bgcolor: "rgba(30,41,59,0.7)", borderRadius: "12px", "& fieldset": { borderColor: "rgba(255,255,255,0.15)" }, "&.Mui-focused fieldset": { borderColor: "#6366f1" } }, "& .MuiInputLabel-root": { color: "#94a3b8" }, "& .MuiFormHelperText-root": { color: "#64748b" } }
      })
    ),
    React.createElement(MaterialUI.DialogActions, { sx: { px: 3, pb: 2 } },
      React.createElement(MaterialUI.Button, {
        variant: "contained", onClick: gui, disabled: dangGui, "aria-label": "Nút lưu khóa API",
        sx: { background: "linear-gradient(135deg, #6366f1, #3b82f6)", borderRadius: "12px", px: 3.5, py: 1.2, fontWeight: 600, textTransform: "none", boxShadow: "0 4px 15px rgba(99,102,241,0.4)" }
      }, dangGui ? "Đang lưu..." : "Lưu khóa")
    )
  );
}

export function setupDialog(sessionId, onDone, thongBao) {
  return React.createElement(NoiDungHopThoai, { sessionId, onDone, thongBao });
}

