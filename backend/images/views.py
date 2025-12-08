# backend/images/views.py

import logging
from django.conf import settings
from rest_framework import viewsets, permissions

from .models import Image
from .serializers import ImageSerializer

logger = logging.getLogger(__name__)


class ImageViewSet(viewsets.ModelViewSet):
    """
    /api/images/ で一覧・作成・更新・削除を扱う ViewSet
    """

    queryset = Image.objects.all().order_by("-created_at")
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        画像アップロード時に呼ばれるフック。
        ここで owner をセットしつつ、GCS への保存状況をログに出す。
        """
        instance = serializer.save(owner=self.request.user)

        logger.warning(
            "Image saved: id=%s name=%s url=%s storage=%s USE_GCS=%s",
            instance.id,
            instance.image.name,  # GCS 上のパス（images/xxx.png）になるはず
            getattr(instance.image, "url", None),
            type(instance.image.storage).__name__,
            getattr(settings, "USE_GCS", None),
        )

        return instance
