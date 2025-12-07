"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { API_BASE_URL } from "@/lib/api";

type ImageItem = {
  id: number;
  title: string;
  image: string;
  created_at: string;
};

export default function ImagesPage() {
  const router = useRouter();
  const [images, setImages] = useState<ImageItem[]>([]);
  const [title, setTitle] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  function getAccessToken(): string | null {
    if (typeof window === "undefined") return null;
    return window.localStorage.getItem("access");
  }

  async function fetchImages() {
    const token = getAccessToken();
    if (!token) {
      router.replace("/auth/login");
      return;
    }

    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/images/`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (res.status === 401) {
        router.replace("/auth/login");
        return;
      }

      if (!res.ok) {
        setError("画像一覧の取得に失敗しました");
        return;
      }

      const data = (await res.json()) as ImageItem[];
      setImages(data);
    } catch (err) {
      setError("通信エラーが発生しました");
    }
  }

  useEffect(() => {
    const token = getAccessToken();
    if (!token) {
      router.replace("/auth/login");
    } else {
      fetchImages();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handleUpload(e: React.FormEvent) {
    e.preventDefault();
    const token = getAccessToken();
    if (!token || !file) {
      setError("タイトルと画像ファイルを指定してください");
      return;
    }

    const formData = new FormData();
    formData.append("title", title);
    formData.append("image", file);

    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API_BASE_URL}/api/images/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`
        },
        body: formData
      });

      if (!res.ok) {
        setError("画像のアップロードに失敗しました");
      } else {
        setTitle("");
        setFile(null);
        await fetchImages();
      }
    } catch (err) {
      setError("通信エラーが発生しました");
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(id: number) {
    const token = getAccessToken();
    if (!token) return;

    try {
      const res = await fetch(`${API_BASE_URL}/api/images/${id}/`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (res.ok || res.status === 204) {
        setImages((prev) => prev.filter((img) => img.id !== id));
      } else {
        setError("削除に失敗しました");
      }
    } catch (err) {
      setError("通信エラーが発生しました");
    }
  }

  function handleLogout() {
    if (typeof window !== "undefined") {
      window.localStorage.removeItem("access");
      window.localStorage.removeItem("refresh");
    }
    router.replace("/auth/login");
  }

  return (
    <main className="min-h-screen max-w-4xl mx-auto py-8 px-4 space-y-8">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">画像一覧</h1>
        <button
          onClick={handleLogout}
          className="px-3 py-1.5 rounded bg-slate-800 border border-slate-700 text-xs text-slate-100"
        >
          ログアウト
        </button>
      </header>

      <section className="bg-slate-900 border border-slate-700 rounded-xl p-4 space-y-3">
        <h2 className="text-sm font-medium text-slate-100 mb-1">
          画像アップロード
        </h2>
        {error && (
          <p className="text-sm text-red-400 bg-red-950/40 px-3 py-2 rounded mb-2">
            {error}
          </p>
        )}
        <form
          onSubmit={handleUpload}
          className="flex flex-col md:flex-row items-start md:items-end gap-3"
        >
          <div className="flex-1 space-y-1 w-full">
            <label className="text-xs text-slate-300">タイトル</label>
            <input
              className="w-full px-3 py-2 rounded bg-slate-800 border border-slate-700 text-sm"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>
          <div className="space-y-1">
            <label className="text-xs text-slate-300">画像ファイル</label>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => {
                const files = e.target.files;
                setFile(files && files[0] ? files[0] : null);
              }}
              className="text-xs"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 rounded bg-emerald-500 hover:bg-emerald-600 text-white text-sm font-medium disabled:opacity-60"
          >
            {loading ? "アップロード中..." : "アップロード"}
          </button>
        </form>
      </section>

      <section className="space-y-3">
        <h2 className="text-sm font-medium text-slate-100">アップロード済み</h2>
        {images.length === 0 ? (
          <p className="text-sm text-slate-400">まだ画像はありません。</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {images.map((img) => {
              const src = img.image.startsWith("http")
                ? img.image
                : `${API_BASE_URL}${img.image}`;
              return (
                <div
                  key={img.id}
                  className="bg-slate-900 border border-slate-700 rounded-lg overflow-hidden flex flex-col"
                >
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={src}
                    alt={img.title || `Image ${img.id}`}
                    className="w-full h-40 object-cover"
                  />
                  <div className="p-3 flex items-center justify-between gap-2">
                    <div className="text-xs text-slate-200 truncate">
                      {img.title || "(no title)"}
                    </div>
                    <button
                      onClick={() => handleDelete(img.id)}
                      className="text-xs px-2 py-1 rounded bg-red-600 text-white"
                    >
                      削除
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </main>
  );
}
