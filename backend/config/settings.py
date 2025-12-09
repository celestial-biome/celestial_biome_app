from pathlib import Path
import os
import json

from corsheaders.defaults import default_headers, default_methods

print("=== DEBUG SETTINGS MODULE:", os.environ.get("DJANGO_SETTINGS_MODULE"))
print("=== DEBUG DJANGO_DEBUG:", os.environ.get("DJANGO_DEBUG"))

# GCS 用（USE_GCS=True のときだけ使う）
try:
    from google.oauth2 import service_account
except ImportError:
    service_account = None

BASE_DIR = Path(__file__).resolve().parent.parent

# =====================
# 基本設定
# =====================

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me-unsafe")

DEBUG = os.environ.get("DJANGO_DEBUG", "").lower() == "true"

# 環境変数 DJANGO_ALLOWED_HOSTS="a.run.app,localhost" みたいな形で指定
_raw_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "")
if _raw_hosts:
    ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(",") if h.strip()]
else:
    ALLOWED_HOSTS = ["*"] if DEBUG else []

# =====================
# アプリケーション
# =====================

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "storages",  # django-storages (GCS)
    "images",    # Celestial Biome の画像アプリ
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    # Cloud Run/Render で WhiteNoise を使うならここ:
    # "whitenoise.middleware.WhiteNoiseMiddleware",
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

# =====================
# DATABASES
# =====================
# ※ 実際の環境に合わせて書き換えてOK。
#   Cloud Run から Render Postgres に繋ぐなら、環境変数から読む形にする。

if os.environ.get("DB_ENGINE"):
    # 例: Cloud Run 用に個別指定するならこちら
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "5432"),
            "NAME": os.environ.get("DB_NAME", "postgres"),
            "USER": os.environ.get("DB_USER", "postgres"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        }
    }
else:
    # ローカル開発用: SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# =====================
# パスワード検証
# =====================

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

# =====================
# 国際化
# =====================

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True

# =====================
# 静的ファイル / メディア
# =====================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# STATICFILES_DIRS = [BASE_DIR / "static"]  # 必要なら

# WhiteNoise を使うなら（任意）
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------- GCS 連携 ----------
USE_GCS = os.environ.get("USE_GCS", "").lower() == "true"

# デフォルト値（ローカルの場合）
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

if USE_GCS:
    # 環境変数：
    # - GS_BUCKET_NAME
    # - GS_CREDENTIALS_JSON （改行なしの JSON をそのまま）
    GS_BUCKET_NAME = os.environ.get("GS_BUCKET_NAME")
    GS_CREDENTIALS_JSON = os.environ.get("GS_CREDENTIALS_JSON")

    if service_account is None:
        raise RuntimeError("google-auth がインストールされていません")

    if not GS_BUCKET_NAME or not GS_CREDENTIALS_JSON:
        raise RuntimeError("GS_BUCKET_NAME と GS_CREDENTIALS_JSON を設定してください")

    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
        json.loads(GS_CREDENTIALS_JSON)
    )

    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_QUERYSTRING_AUTH = False  # 公開URLをクエリなしで
    # 必要に応じて:
    # GS_PROJECT_ID = os.environ.get("GS_PROJECT_ID")

    MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/"

# デバッグログ（必要なら）
print("=== DEBUG USE_GCS:", USE_GCS)
print("=== DEBUG DEFAULT_FILE_STORAGE:", DEFAULT_FILE_STORAGE)
print("=== DEBUG MEDIA_URL:", MEDIA_URL)

# =====================
# REST FRAMEWORK / JWT
# =====================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# =====================
# CORS / CSRF
# =====================

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# CORS_ALLOWED_ORIGINS = [
#     "https://celestial-biome-app-front.onrender.com",
# ]

CSRF_TRUSTED_ORIGINS = [
    "https://celestial-biome-app-front.onrender.com",
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    "content-type",
    "authorization",
    "x-csrftoken",
    "x-requested-with",
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# =====================
# ロギング（任意）
# =====================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # ここが重要！CORSの動作を詳細にログに出す設定
        'corsheaders': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
