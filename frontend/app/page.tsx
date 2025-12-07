import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center gap-4">
      <h1 className="text-3xl font-bold">Celestial Biome Prototype</h1>
      <p className="text-sm text-slate-300">
        ユーザー登録・ログイン・画像アップロードの最小構成です。
      </p>
      <div className="flex gap-4 mt-4">
        <Link
          href="/auth/register"
          className="px-4 py-2 rounded bg-sky-500 text-white text-sm font-medium"
        >
          新規登録
        </Link>
        <Link
          href="/auth/login"
          className="px-4 py-2 rounded bg-slate-700 text-white text-sm font-medium"
        >
          ログイン
        </Link>
        <Link
          href="/images"
          className="px-4 py-2 rounded bg-emerald-500 text-white text-sm font-medium"
        >
          画像一覧
        </Link>
      </div>
    </main>
  );
}
