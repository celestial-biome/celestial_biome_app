import os
from pathlib import Path
from datetime import timedelta


import dj_database_url

# =============================================================================
# 基本設定
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-change-me",  # 開発用。本番では必ず環境変数で上書き
)

DEBUG = os.environ.get("DJANGO_DEBUG", "").lower() == "true"

# 例: DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,celestial-biome-app.onrender.com
_raw_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "")
if _raw_hosts:
    ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(",") if h.strip()]
else:
    ALLOWED_HOSTS = ["*"] if DEBUG else []

# =============================================================================
# アプリケーション
# =============================================================================

INSTALLED_APPS = [
    # サードパーティ
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",

    # Django 標準
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # プロジェクト内アプリ
    "accounts",
    "images",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # ★ 最初の方に入れる
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# =============================================================================
# データベース
# =============================================================================

# Render / 本番では DATABASE_URL を env で渡す
# 例: postgres://user:password@host:5432/dbname
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgres://cb_user:cb_password@db:5432/celestial_biome_dev",  # ローカル docker-compose 用
)

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# =============================================================================
# 認証 / REST Framework / JWT
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# =============================================================================
# 国際化 / タイムゾーン
# =============================================================================

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True
USE_TZ = True

# =============================================================================
# 静的ファイル / メディア
# =============================================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# デフォルトはローカルディスク
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# =============================================================================
# CORS
# =============================================================================

CORS_ALLOW_CREDENTIALS = True

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False
    raw_origins = os.environ.get("CORS_ALLOWED_ORIGINS", "")
    CORS_ALLOWED_ORIGINS = [
        o.strip() for o in raw_origins.split(",") if o.strip()
    ]
    # 追加でヘッダ許可（念のため）
    from corsheaders.defaults import default_headers

    CORS_ALLOW_HEADERS = list(default_headers) + [
        "authorization",
        "content-type",
    ]

# =============================================================================
# GCS ストレージ（オプション）
# =============================================================================

# 環境変数 USE_GCS が "true" / "True" / "1" / "yes" のときだけ GCS を使う
USE_GCS = os.environ.get("USE_GCS", "").lower() in ("true", "1", "yes")

if USE_GCS:
    INSTALLED_APPS += ["storages"]

    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

    GS_BUCKET_NAME = os.environ.get("GS_BUCKET_NAME")
    if not GS_BUCKET_NAME:
        raise RuntimeError("USE_GCS=True の場合、GS_BUCKET_NAME が必要です。")

    # GCS の公開 URL
    MEDIA_URL = os.environ.get(
        "MEDIA_URL",
        f"https://storage.googleapis.com/{GS_BUCKET_NAME}/",
    )

    from google.oauth2 import service_account
    import json

    GS_CREDENTIALS_JSON = os.environ.get("GS_CREDENTIALS_JSON", "")
    if not GS_CREDENTIALS_JSON:
        raise RuntimeError("USE_GCS=True の場合、GS_CREDENTIALS_JSON が必要です。")

    try:
        info = json.loads(GS_CREDENTIALS_JSON)
    except json.JSONDecodeError as e:
        raise RuntimeError("GS_CREDENTIALS_JSON が正しい JSON ではありません。") from e

    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(info)

# =============================================================================
# その他
# =============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


print("=== DEBUG: USE_GCS =", USE_GCS)

if USE_GCS:
    print("=== DEBUG: DEFAULT_FILE_STORAGE should be GCS")
    print("=== DEBUG: GS_BUCKET_NAME =", os.environ.get("GS_BUCKET_NAME"))
else:
    print("=== DEBUG: USING LOCAL MEDIA (FileSystemStorage)")



print("=== DEBUG USE_GCS:", USE_GCS)
print("=== DEBUG DEFAULT_FILE_STORAGE:", globals().get("DEFAULT_FILE_STORAGE", "(not set)"))
print("=== DEBUG MEDIA_URL:", MEDIA_URL)