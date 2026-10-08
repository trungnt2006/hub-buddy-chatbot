import React, { useState, useEffect } from 'react';
import { 
  Sidebar 
} from './components/Sidebar';
import { 
  MessageList 
} from './components/MessageList';
import { 
  ChatInput 
} from './components/ChatInput';
import { 
  SetupModal 
} from './components/SetupModal';
import { 
  getSessionId, 
  checkStatus, 
  sendMessage, 
  resetChat 
} from './api';
import { 
  Menu, 
  RotateCcw, 
  KeyRound
} from 'lucide-react';

export default function App() {
  const [sessionId] = useState(() => getSessionId());
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [showSetup, setShowSetup] = useState(false);
  const [setupPrompt, setSetupPrompt] = useState('');
  const [modelName, setModelName] = useState('space-bunny-free');

  useEffect(() => {
    checkStatus().then((res) => {
      if (res.ok && res.data) {
        if (!res.data.configured) {
          setShowSetup(true);
        }
      }
    });
  }, []);

  const handleSend = async (overrideText) => {
    const textToSend = (overrideText || input).trim();
    if (!textToSend || isLoading) return;

    const nextMessages = [...messages, { role: 'user', content: textToSend }];
    setMessages(nextMessages);
    setInput('');
    setIsLoading(true);
    setError('');

    const res = await sendMessage(sessionId, textToSend);
    setIsLoading(false);

    if (res.ok && res.data && res.data.reply) {
      setMessages([...nextMessages, { role: 'assistant', content: res.data.reply }]);
    } else {
      const errMsg = (res.data && res.data.message) || 'Có lỗi xảy ra khi xử lý phản hồi.';
      setError(errMsg);
      if (res.status === 400 || (res.data && res.data.code === 'missing_api_key')) {
        setSetupPrompt(errMsg);
        setShowSetup(true);
      }
    }
  };

  const handleNewChat = async () => {
    const res = await resetChat(sessionId);
    if (res.ok) {
      setMessages([]);
      setError('');
    } else {
      setError('Không thể làm mới đoạn chat.');
    }
  };

  const handleRetry = () => {
    if (messages.length === 0) return;
    const lastUser = [...messages].reverse().find((m) => m.role === 'user');
    if (lastUser) {
      handleSend(lastUser.content);
    }
  };

  return (
    <div className="flex h-screen w-full bg-[#09090b] text-zinc-100 overflow-hidden relative">
      {/* Sidebar */}
      <Sidebar
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        onNewChat={handleNewChat}
        onSelectPrompt={(prompt) => handleSend(prompt)}
        onOpenSettings={() => setShowSetup(true)}
        modelName={modelName}
      />

      {/* Main Clean Canvas */}
      <main className="flex-1 flex flex-col h-full min-w-0 relative">
        {/* Top Navbar */}
        <header className="h-14 flex items-center justify-between px-4 border-b border-zinc-800/80 bg-[#0c0d10] shrink-0">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 text-zinc-400 hover:text-zinc-200 rounded-lg hover:bg-zinc-800/60 transition"
              title="Mở / Đóng thanh bên"
            >
              <Menu className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-2">
              <span className="font-semibold text-sm text-zinc-100">
                HUB-Buddy
              </span>
              <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-zinc-800/80 border border-zinc-700/60 text-[11px] text-zinc-300">
                <span className="size-1.5 rounded-full bg-emerald-400" />
                <span>OpenCode · {modelName}</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleNewChat}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-300 hover:text-white hover:bg-zinc-800 transition border border-zinc-800 hover:border-zinc-700"
              title="Bắt đầu đoạn chat mới"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Làm mới</span>
            </button>
            <button
              onClick={() => setShowSetup(true)}
              className="p-2 text-zinc-400 hover:text-zinc-200 rounded-lg hover:bg-zinc-800 transition border border-transparent hover:border-zinc-800"
              title="Cài đặt khóa API"
            >
              <KeyRound className="w-4 h-4" />
            </button>
          </div>
        </header>

        {/* Message Stream */}
        <MessageList
          messages={messages}
          isLoading={isLoading}
          error={error}
          onSelectPrompt={(p) => handleSend(p)}
          onRetry={handleRetry}
        />

        {/* Floating Bottom Composer */}
        <ChatInput
          value={input}
          onChange={setInput}
          onSend={() => handleSend()}
          onStop={() => setIsLoading(false)}
          disabled={isLoading}
          isLoading={isLoading}
        />
      </main>

      {/* Setup API Modal */}
      {showSetup && (
        <SetupModal
          sessionId={sessionId}
          onClose={() => setShowSetup(false)}
          onSaved={() => {
            setShowSetup(false);
            setSetupPrompt('');
          }}
          initialMessage={setupPrompt}
        />
      )}
    </div>
  );
}
