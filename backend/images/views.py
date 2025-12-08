# backend/images/views.py

import logging
from django.conf import settings
from rest_framework import viewsets, permissions

from .models import Image
from .serializers import ImageSerializer

logger = logging.getLogger(__name__)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all().order_by("-created_at")
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)

        # 内側の実ストレージのクラス名（GoogleCloudStorage かどうか）
        storage_backend = getattr(
            instance.image.storage, "_wrapped", instance.image.storage
        )

        # 「その名前のファイルがストレージ上に存在するか？」を GCS に聞く
        exists = instance.image.storage.exists(instance.image.name)

        logger.warning(
            "Image saved: id=%s name=%s url=%s storage=%s backend=%s USE_GCS=%s exists=%s",
            instance.id,
            instance.image.name,
            getattr(instance.image, "url", None),
            type(instance.image.storage).__name__,
            type(storage_backend).__name__,
            getattr(settings, "USE_GCS", None),
            exists,
        )

        return instance
