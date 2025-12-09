# ベースイメージ
FROM python:3.11

# Python の基本設定
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ★ 以下の行を追加してください（キャッシュ破棄用のおまじない）
RUN echo "Cache bust: 2025-12-09-reset"

# 作業ディレクトリ
WORKDIR /app

# 必要ならビルドツール（psycopg2 など用）
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*

# ここで backend 配下の requirements.txt をコピー
# └ Cloud Build の build context を `backend` にしている前提
COPY requirements.txt .

# ライブラリインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体をコピー
COPY . .

# 環境変数（Cloud Run から PORT が渡される）
ENV PORT=8080

# 静的ファイルを使うなら（任意）
# RUN python manage.py collectstatic --noinput

# Cloud Run 用エントリポイント
# PORT が Cloud Run から渡されるので、それを使って bind
CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --access-logfile - --error-logfile -"]
