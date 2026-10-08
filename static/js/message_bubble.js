// Định dạng tin nhắn theo chuẩn spec chat.md: tin người dùng căn phải, bot trải thẳng mép trái.
export function messageBubble(role, content, khoa) {
  const laNguoi = role === "human";

  if (laNguoi) {
    return React.createElement(
      MaterialUI.Box,
      { key: khoa, sx: { display: "flex", justifyContent: "flex-end", my: 2.5, width: "100%" } },
      React.createElement(
        MaterialUI.Box,
        {
          className: "fade-in",
          sx: {
            maxWidth: { xs: "85%", sm: "75%" },
            bgcolor: "#27272a",
            color: "#f8fafc",
            px: 2.5,
            py: 1.5,
            borderRadius: "20px",
            fontSize: "0.95rem",
            lineHeight: 1.6,
            whiteSpace: "pre-wrap",
            wordBreak: "break-word",
            border: "1px solid rgba(255, 255, 255, 0.08)",
          },
        },
        String(content)
      )
    );
  }

  // Tin trợ lý AI: thẳng mép trái cột, không avatar thừa, typography thoáng đẹp
  return React.createElement(
    MaterialUI.Box,
    { key: khoa, sx: { display: "flex", flexDirection: "column", my: 3, width: "100%" } },
    React.createElement(
      MaterialUI.Typography,
      { variant: "caption", sx: { color: "#10b981", fontWeight: 600, mb: 1, letterSpacing: "0.02em" } },
      "HUB-Buddy"
    ),
    React.createElement(
      MaterialUI.Box,
      {
        className: "fade-in",
        sx: {
          color: "#f1f5f9",
          fontSize: "1rem",
          lineHeight: 1.75,
          letterSpacing: "0.01em",
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
        },
      },
      String(content)
    )
  );
}



