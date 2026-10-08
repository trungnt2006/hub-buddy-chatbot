// Bộ Icon SVG vector độ phân giải cao, không phụ thuộc font ligature ngoài.
function svg(paths, size = 20, color = "currentColor", vb = "0 0 24 24") {
  return React.createElement(
    "svg",
    {
      width: size,
      height: size,
      viewBox: vb,
      fill: "none",
      stroke: color,
      strokeWidth: "2",
      strokeLinecap: "round",
      strokeLinejoin: "round",
      style: { display: "inline-block", verticalAlign: "middle", flexShrink: 0 },
    },
    paths.map((d, i) => React.createElement("path", { key: i, d }))
  );
}

export const IconBot = (s, c) =>
  svg(["M12 8V4H8", "M4 8h16v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8z", "M9 13v2", "M15 13v2"], s, c);

export const IconUser = (s, c) =>
  svg(["M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2", "M12 3a4 4 0 1 0 0 8 4 4 0 0 0 0-8z"], s, c);

export const IconSend = (s, c) =>
  svg(["M22 2L11 13", "M22 2l-7 20-4-9-9-4 20-7z"], s, c);

export const IconReset = (s, c) =>
  svg(["M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8", "M21 3v5h-5", "M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16", "M3 21v-5h5"], s, c);

export const IconCalendar = (s, c) =>
  svg(["M19 4H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z", "M16 2v4", "M8 2v4", "M3 10h18"], s, c);

export const IconBrain = (s, c) =>
  svg(["M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-2.04z"], s, c);

export const IconBook = (s, c) =>
  svg(["M4 19.5A2.5 2.5 0 0 1 6.5 17H20", "M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"], s, c);

export const IconSparkles = (s, c) =>
  svg(["M12 3l1.912 5.885L20 10.5l-5.088 3.615L16.824 20 12 16.385 7.176 20l1.912-5.885L4 10.5l6.088-1.615L12 3z"], s, c);

export const IconKey = (s, c) =>
  svg(["M21 2l-2 2m-1.5 1.5L14 9l-1.5-1.5L11 9l-1-1-4 4a5 5 0 1 0 7 7l4-4-1-1 1.5-1.5-1.5-1.5L19 7l1.5-1.5L22 4l-1-2z"], s, c);

export const IconArrowUp = (s, c) =>
  svg(["M12 19V5", "M5 12l7-7 7 7"], s, c);

