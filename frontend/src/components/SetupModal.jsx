import React, { useState } from 'react';
import { KeyRound, Check, AlertCircle, X, ShieldCheck } from 'lucide-react';
import { saveApiKey } from '../api';

export function SetupModal({ sessionId, onClose, onSaved, initialMessage }) {
  const [key, setKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(initialMessage || '');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const clean = key.trim();
    if (!clean) return;
    setLoading(true);
    setError('');
    const res = await saveApiKey(clean, sessionId);
    setLoading(false);
    if (res.ok) {
      onSaved();
      onClose();
    } else {
      setError((res.data && res.data.message) || 'Khóa không hợp lệ.');
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-xs animate-in fade-in duration-200">
      <div className="relative w-full max-w-md rounded-2xl border border-zinc-800 bg-[#141417] p-6 shadow-2xl text-zinc-100">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 text-zinc-400 hover:text-white rounded-lg hover:bg-zinc-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-3 mb-4">
          <div className="p-2.5 rounded-xl bg-zinc-800 border border-zinc-700/60 text-zinc-200">
            <KeyRound className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-semibold text-base text-zinc-100">
              Cấu hình API Key
            </h3>
            <p className="text-xs text-zinc-400">Kết nối OpenCode AI hoặc OpenAI</p>
          </div>
        </div>

        {error && (
          <div className="mb-4 flex items-start gap-2.5 rounded-xl border border-rose-500/20 bg-rose-500/10 p-3 text-sm text-rose-300">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-zinc-300 mb-1.5">
              Khóa API Key
            </label>
            <input
              type="password"
              value={key}
              onChange={(e) => setKey(e.target.value)}
              placeholder="oc_sk_... hoặc sk-..."
              required
              className="w-full rounded-xl border border-zinc-700 bg-zinc-900 px-3.5 py-2.5 text-sm text-zinc-100 placeholder:text-zinc-500 focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500 outline-none transition"
            />
          </div>

          <div className="flex items-center gap-2 text-xs text-zinc-400 bg-zinc-900/60 p-2.5 rounded-xl border border-zinc-800">
            <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Khóa được lưu cục bộ an toàn trong tệp .env trên máy bạn.</span>
          </div>

          <div className="flex justify-end gap-2.5 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-zinc-400 hover:text-white rounded-xl hover:bg-zinc-800 transition"
            >
              Hủy
            </button>
            <button
              type="submit"
              disabled={loading || !key.trim()}
              className="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-zinc-950 bg-zinc-100 hover:bg-white rounded-xl transition disabled:opacity-30 disabled:cursor-not-allowed"
            >
              {loading ? 'Đang lưu...' : 'Lưu và tiếp tục'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
