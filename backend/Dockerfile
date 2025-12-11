# backend/Dockerfile
FROM ghcr.io/astral-sh/uv:python3.11-bookworm

# Python の基本設定
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 【重要】 uv が作成する仮想環境のパスを固定する
# これを設定すると uv sync は .venv ではなくここに環境を作ります
ENV UV_PROJECT_ENVIRONMENT="/opt/venv"

# パスを通す（これで python や pytest コマンドがそのまま使えます）
ENV PATH="$UV_PROJECT_ENVIRONMENT/bin:$PATH"

WORKDIR /app

# 必要なビルドツール
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*

# 依存関係定義ファイルのコピー
# uv.lock がまだない場合でもビルドできるように pyproject.toml だけ先にコピー
COPY pyproject.toml uv.lock* ./

# 【重要】 ライブラリのインストール (uv sync)
# --frozen: uv.lock があればそれを厳密に守る（なければエラーになるので初回は外しても良いが、通常はlockファイルを含める）
# --no-install-project: プロジェクト自体（djangoアプリ）はインストールせず、ライブラリだけ入れる
RUN uv sync --no-install-project

# ソースコードのコピー
COPY . .

ENV PORT=8000

# venvにパスが通っているので、そのままコマンドを叩けばOK
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-"]