import React from 'react';
import { 
  Plus, 
  Sparkles, 
  Calendar, 
  Brain, 
  Settings, 
  GraduationCap, 
  ChevronLeft,
  ChevronRight,
  Bot
} from 'lucide-react';

export function Sidebar({ 
  isOpen, 
  onToggle, 
  onNewChat, 
  onSelectPrompt, 
  onOpenSettings, 
  modelName = "space-bunny-free" 
}) {
  const quickTopics = [
    { title: "Lên lịch ôn thi tuần này", icon: Calendar },
    { title: "Kỹ thuật Pomodoro & Feynman", icon: Brain },
    { title: "Tóm tắt bài học trọng tâm", icon: Sparkles },
    { title: "Hướng dẫn giải bài tập khó", icon: GraduationCap },
  ];

  return (
    <aside
      className={`fixed md:static inset-y-0 left-0 z-40 flex flex-col bg-[#0c0d10] border-r border-zinc-800/80 transition-all duration-300 ease-in-out ${
        isOpen ? "w-64" : "w-0 md:w-16"
      } overflow-hidden`}
    >
      {/* Top Header / Brand */}
      <div className="h-14 flex items-center justify-between px-3.5 border-b border-zinc-800/80">
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="size-8 rounded-xl bg-zinc-800 border border-zinc-700/60 flex items-center justify-center text-zinc-100 shadow-sm shrink-0">
            <Bot className="w-4 h-4" />
          </div>
          {isOpen && (
            <div className="min-w-0">
              <span className="font-semibold text-sm tracking-tight text-zinc-100 block truncate">
                HUB-Buddy
              </span>
              <span className="text-[11px] text-zinc-400 font-medium block truncate">
                Trợ lý học tập
              </span>
            </div>
          )}
        </div>
        <button
          onClick={onToggle}
          className="p-1.5 text-zinc-400 hover:text-zinc-200 rounded-lg hover:bg-zinc-800/60 transition-colors hidden md:block"
          title={isOpen ? "Thu gọn thanh bên" : "Mở rộng thanh bên"}
        >
          {isOpen ? <ChevronLeft className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
        </button>
      </div>

      {/* New Chat Button */}
      <div className="p-3">
        <button
          onClick={onNewChat}
          className="w-full flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl bg-zinc-800/80 hover:bg-zinc-800 text-zinc-200 border border-zinc-700/50 hover:border-zinc-600 transition-all text-xs font-medium group"
        >
          <Plus className="w-4 h-4 group-hover:rotate-90 transition-transform duration-200 text-zinc-300" />
          {isOpen && <span>Đoạn chat mới</span>}
        </button>
      </div>

      {/* Quick Prompts Navigation */}
      <div className="flex-1 overflow-y-auto px-2 py-1 space-y-1">
        {isOpen && (
          <div className="px-2.5 py-1.5 text-[10px] font-semibold uppercase tracking-wider text-zinc-500">
            Gợi ý học tập
          </div>
        )}
        {quickTopics.map((topic, i) => {
          const Icon = topic.icon;
          return (
            <button
              key={i}
              onClick={() => onSelectPrompt(topic.title)}
              className="w-full flex items-center gap-2.5 px-2.5 py-2 rounded-xl text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800/60 transition-all text-xs text-left group"
              title={topic.title}
            >
              <Icon className="w-4 h-4 shrink-0 text-zinc-400 group-hover:text-zinc-200 transition-colors" />
              {isOpen && <span className="truncate">{topic.title}</span>}
            </button>
          );
        })}
      </div>

      {/* Bottom Footer: Model Info & Settings */}
      <div className="p-3 border-t border-zinc-800/80 bg-black/20 space-y-2">
        {isOpen && (
          <div className="flex items-center justify-between px-2.5 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-[11px] text-zinc-400">
            <div className="flex items-center gap-1.5 truncate">
              <span className="size-2 rounded-full bg-emerald-500 shadow-xs" />
              <span className="truncate font-mono text-[10px] text-zinc-300">{modelName}</span>
            </div>
            <span className="text-[10px] text-emerald-400 font-medium">Sẵn sàng</span>
          </div>
        )}
        <button
          onClick={onOpenSettings}
          className="w-full flex items-center gap-2 px-2.5 py-2 rounded-xl text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50 transition-colors text-xs text-left"
          title="Cấu hình API Key"
        >
          <Settings className="w-4 h-4 shrink-0 text-zinc-400 hover:text-zinc-200" />
          {isOpen && <span>Cài đặt API Key</span>}
        </button>
      </div>
    </aside>
  );
}
