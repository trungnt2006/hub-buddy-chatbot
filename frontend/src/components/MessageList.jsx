import React, { useState } from 'react';
import { 
  Copy, 
  Check, 
  Sparkles, 
  Calendar, 
  Brain, 
  GraduationCap, 
  AlertCircle,
  RotateCcw,
  Bot
} from 'lucide-react';

export function MessageList({ 
  messages, 
  isLoading, 
  error, 
  onSelectPrompt, 
  onRetry 
}) {
  const [copiedIndex, setCopiedIndex] = useState(null);

  const handleCopy = (text, idx) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(idx);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const starterCards = [
    {
      title: "Lên lịch ôn thi tuần này",
      desc: "Phân bổ thời gian học hợp lý theo từng môn và ngày thi",
      icon: Calendar,
    },
    {
      title: "Kỹ thuật Pomodoro & Feynman",
      desc: "Tăng khả năng tập trung và hiểu sâu bài học khó",
      icon: Brain,
    },
    {
      title: "Tóm tắt bài học trọng tâm",
      desc: "Chắt lọc công thức, định lý và luận điểm cốt lõi",
      icon: Sparkles,
    },
    {
      title: "Hướng dẫn giải bài tập khó",
      desc: "Từng bước phân tích logic và tìm phương pháp giải",
      icon: GraduationCap,
    }
  ];

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-6 max-w-2xl mx-auto w-full text-center">
        {/* Minimal Hero Logo */}
        <div className="size-12 rounded-2xl bg-zinc-800 border border-zinc-700/60 flex items-center justify-center text-zinc-100 mb-4 shadow-xs">
          <Bot className="w-6 h-6 text-zinc-200" />
        </div>

        <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight text-zinc-100 mb-2">
          HUB-Buddy Học Tập AI
        </h1>
        <p className="text-sm text-zinc-400 max-w-md mx-auto mb-8 leading-relaxed">
          Trợ lý AI hỗ trợ giải đề, lên lịch ôn thi và tóm tắt kiến thức cho sinh viên.
        </p>

        {/* 2x2 Minimal Starter Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full text-left">
          {starterCards.map((card, i) => {
            const Icon = card.icon;
            return (
              <button
                key={i}
                onClick={() => onSelectPrompt(card.title)}
                className="group flex flex-col p-4 rounded-xl border border-zinc-800 bg-[#121316] hover:bg-[#18191d] hover:border-zinc-700 transition-all cursor-pointer"
              >
                <div className="flex items-center gap-2.5 mb-1.5">
                  <div className="p-1.5 rounded-lg bg-zinc-800 text-zinc-300 group-hover:text-white transition-colors">
                    <Icon className="w-4 h-4" />
                  </div>
                  <h3 className="font-medium text-sm text-zinc-200 group-hover:text-white transition-colors">
                    {card.title}
                  </h3>
                </div>
                <p className="text-xs text-zinc-400 pl-9 line-clamp-2 leading-relaxed">
                  {card.desc}
                </p>
              </button>
            );
          })}
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6">
      <div className="max-w-3xl mx-auto w-full space-y-6">
        {messages.map((msg, idx) => {
          const isUser = msg.role === 'user';
          if (isUser) {
            return (
              <div key={idx} className="flex justify-end">
                <div className="max-w-[80%] rounded-2xl bg-[#27272a] text-zinc-100 px-4 py-2.5 text-base border border-zinc-700/40 whitespace-pre-wrap [overflow-wrap:anywhere]">
                  {msg.content}
                </div>
              </div>
            );
          }

          // Assistant message: Clean typography per chat.md, aligned left, no bulky avatar
          return (
            <div key={idx} className="group relative max-w-2xl text-left space-y-2">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-semibold text-zinc-400 tracking-wider uppercase">
                  HUB-Buddy AI
                </span>
              </div>
              <div className="text-base text-zinc-200 leading-relaxed whitespace-pre-wrap [overflow-wrap:anywhere]">
                {msg.content}
              </div>

              {/* Action bar on hover */}
              <div className="flex items-center gap-2 pt-1 opacity-80 group-hover:opacity-100 transition-opacity">
                <button
                  onClick={() => handleCopy(msg.content, idx)}
                  className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 transition"
                  title="Sao chép câu trả lời"
                >
                  {copiedIndex === idx ? (
                    <>
                      <Check className="w-3.5 h-3.5 text-emerald-400" />
                      <span className="text-emerald-400">Đã chép</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-3.5 h-3.5" />
                      <span>Sao chép</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          );
        })}

        {/* Loading state */}
        {isLoading && (
          <div className="flex items-center gap-2 py-2 text-zinc-400 text-sm">
            <span className="size-2 rounded-full bg-zinc-400 animate-pulse" />
            <span>HUB-Buddy đang soạn câu trả lời...</span>
          </div>
        )}

        {/* Error notification */}
        {error && (
          <div className="flex items-start justify-between gap-3 p-4 rounded-xl border border-rose-500/20 bg-rose-500/10 text-sm text-rose-300">
            <div className="flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-rose-400" />
              <span>{error}</span>
            </div>
            {onRetry && (
              <button
                onClick={onRetry}
                className="flex items-center gap-1 text-xs text-rose-300 hover:text-white px-2 py-1 rounded-lg bg-rose-500/20 hover:bg-rose-500/30 transition shrink-0"
              >
                <RotateCcw className="w-3 h-3" />
                Thử lại
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
