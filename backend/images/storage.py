# backend/images/storage.py

from django.conf import settings
from django.core.files.storage import FileSystemStorage

try:
    # django-storages の GCS バックエンド
    from storages.backends.gcloud import GoogleCloudStorage
except ImportError:
    GoogleCloudStorage = None


def get_image_storage():
    """
    画像用のストレージを返す。
    - USE_GCS=True かつ GoogleCloudStorage が使える → GCS
    - それ以外 → ローカル FileSystemStorage
    """
    use_gcs = getattr(settings, "USE_GCS", False)

    if use_gcs and GoogleCloudStorage is not None:
        # GS_BUCKET_NAME や GS_CREDENTIALS は settings 側の設定を利用
        return GoogleCloudStorage()

    # ローカル（開発 or GCS 無効時）のフォールバック
    return FileSystemStorage(location=settings.MEDIA_ROOT)
