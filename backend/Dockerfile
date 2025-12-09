# ベースイメージ
FROM ghcr.io/astral-sh/uv:python3.11-bookworm

# Python の基本設定
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 【追記 1】 venv の場所を定義し、パスを通す
# これにより、以降の python コマンドは自動的に venv 内のものを参照します
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 作業ディレクトリ
WORKDIR /app

# 必要ならビルドツール（psycopg2 など用）
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*

# ここで backend 配下の requirements.txt をコピー
COPY requirements.txt .

# 【追記 2】 venv を作成
# uv venv は python -m venv より高速です
RUN uv venv $VIRTUAL_ENV

# 【変更】 ライブラリインストール
# --system オプションを削除しました（venv にインストールするため）
RUN uv pip install --no-cache -r requirements.txt

# アプリ本体をコピー
COPY . .

# 環境変数
ENV PORT=8080

# Cloud Run 用エントリポイント
# パスが通っているため、venv 内の gunicorn が自動的に使われます
CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --access-logfile - --error-logfile -"]