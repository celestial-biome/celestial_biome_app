from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.core.files.storage import FileSystemStorage
from pathlib import Path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/", include("images.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# cb_image_storage = FileSystemStorage(
#     location=settings.BASE_DIR / "media/images",  # ここに保存
#     base_url="/media/images/"                        # ここから配信
# )