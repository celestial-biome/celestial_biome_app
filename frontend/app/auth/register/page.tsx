"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { API_BASE_URL } from "@/lib/api";

export default function RegisterPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE_URL}/api/auth/register/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password })
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data.detail || "登録に失敗しました");
      } else {
        router.push("/auth/login");
      }
    } catch (err) {
      setError("通信エラーが発生しました");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md bg-slate-900 border border-slate-700 rounded-xl p-6 space-y-4"
      >
        <h1 className="text-xl font-semibold text-center mb-2">
          ユーザー登録
        </h1>

        {error && (
          <p className="text-sm text-red-400 bg-red-950/40 px-3 py-2 rounded">
            {error}
          </p>
        )}

        <div className="space-y-1">
          <label className="text-sm text-slate-200">ユーザー名</label>
          <input
            className="w-full px-3 py-2 rounded bg-slate-800 border border-slate-700 text-sm"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="space-y-1">
          <label className="text-sm text-slate-200">メールアドレス</label>
          <input
            type="email"
            className="w-full px-3 py-2 rounded bg-slate-800 border border-slate-700 text-sm"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className="space-y-1">
          <label className="text-sm text-slate-200">パスワード</label>
          <input
            type="password"
            className="w-full px-3 py-2 rounded bg-slate-800 border border-slate-700 text-sm"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full mt-2 px-4 py-2 rounded bg-sky-500 hover:bg-sky-600 text-white text-sm font-medium disabled:opacity-60"
        >
          {loading ? "登録中..." : "登録"}
        </button>
      </form>
    </main>
  );
}
