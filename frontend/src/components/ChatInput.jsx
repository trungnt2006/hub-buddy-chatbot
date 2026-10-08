import React, { useRef, useEffect } from 'react';
import { ArrowUp, Square } from 'lucide-react';

export function ChatInput({ 
  value, 
  onChange, 
  onSend, 
  onStop, 
  disabled, 
  isLoading 
}) {
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [value]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!disabled && value.trim()) {
        onSend();
      }
    }
  };

  return (
    <div className="shrink-0 px-4 pb-4 pt-1 bg-gradient-to-t from-[#09090b] via-[#09090b]/90 to-transparent">
      <div className="max-w-3xl mx-auto w-full">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            if (!disabled && value.trim()) onSend();
          }}
          className="flex items-end gap-2 p-2 rounded-3xl border border-zinc-800 bg-[#141417] focus-within:border-zinc-600 focus-within:ring-1 focus-within:ring-zinc-600 transition shadow-lg"
        >
          <textarea
            ref={textareaRef}
            rows={1}
            value={value}
            disabled={disabled}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Đặt câu hỏi về môn học, bài tập hoặc ôn thi..."
            className="flex-1 max-h-48 min-h-[38px] resize-none bg-transparent px-3 py-2 text-base text-zinc-100 placeholder:text-zinc-500 outline-none leading-normal"
          />

          {isLoading ? (
            <button
              type="button"
              onClick={onStop}
              className="grid size-10 shrink-0 cursor-pointer place-items-center rounded-2xl bg-zinc-700 hover:bg-zinc-600 text-white outline-none transition"
              title="Dừng trả lời"
            >
              <Square className="w-3.5 h-3.5 fill-current" />
            </button>
          ) : (
            <button
              type="submit"
              disabled={disabled || !value.trim()}
              className="grid size-10 shrink-0 cursor-pointer place-items-center rounded-2xl bg-zinc-100 hover:bg-white text-zinc-900 outline-none transition disabled:opacity-20 disabled:cursor-not-allowed"
              title="Gửi câu hỏi"
            >
              <ArrowUp className="w-4 h-4 stroke-[2.5]" />
            </button>
          )}
        </form>

        <p className="mt-2 text-center text-[11px] text-zinc-500 font-medium">
          Nhấn <kbd className="px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 border border-zinc-700/60">Enter</kbd> gửi · <kbd className="px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 border border-zinc-700/60">Shift + Enter</kbd> xuống dòng
        </p>
      </div>
    </div>
  );
}
