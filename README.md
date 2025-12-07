# Celestial Biome Prototype

Backend: Django REST Framework (JWT 認証, ユーザー登録, 画像アップロード)
Frontend: Next.js (App Router) + TypeScript + Tailwind CSS
DB: PostgreSQL (ローカルでは Docker コンテナ, 本番は Render PostgreSQL を想定)

## ローカル開発

```bash
docker compose build
docker compose up
```

- Backend API: http://localhost:8000/
- Frontend: http://localhost:3000/

Backend の主なエンドポイント:

- `POST /api/auth/register/` ユーザー登録（username, email, password）
- `POST /api/auth/token/` JWT ログイン（username, password）
- `GET /api/auth/me/` ログインユーザー情報
- `GET /api/images/` 画像一覧（認証必須）
- `POST /api/images/` 画像アップロード（multipart/form-data, 認証必須）
- `DELETE /api/images/{id}/` 画像削除（認証必須）

フロントエンドは `NEXT_PUBLIC_API_BASE_URL` を使って Backend にアクセスします。

## Render デプロイのイメージ

- Render PostgreSQL を作成し、`DATABASE_URL` を取得
- Backend 用 Web Service:
  - Root: `backend`
  - Runtime: Docker
  - Dockerfile: `backend/Dockerfile`
  - 環境変数: `DATABASE_URL` などを設定
- Frontend 用 Web Service:
  - Root: `frontend`
  - Runtime: Docker
  - Dockerfile: `frontend/Dockerfile`
  - 環境変数: `NEXT_PUBLIC_API_BASE_URL` に Backend の URL を設定

画像ファイルはプロトタイプとしては Django のローカルファイルシステム上に保存しています。
Render 本番ではコンテナファイルシステムは揮発的なので、
本格運用では GCS / S3 など外部ストレージに切り替える前提で設計してください。
