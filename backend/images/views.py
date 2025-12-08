# backend/images/views.py

import logging
from django.conf import settings
from rest_framework import generics, permissions

from .models import Image
from .serializers import ImageSerializer

logger = logging.getLogger(__name__)

class ImageListCreateView(generics.ListCreateAPIView):
    queryset = Image.objects.all().order_by("-created_at")
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)

        # ここで「Django がどう認識しているか」を全部ログに吐く
        logger.warning(
            "Image saved: id=%s name=%s url=%s storage=%s USE_GCS=%s",
            instance.id,
            instance.image.name,         # GCS 上のパスになるはず（images/xxx.png）
            getattr(instance.image, "url", None),  # GCS の URL になるはず
            type(instance.image.storage).__name__, # GoogleCloudStorage になってるか？
            getattr(settings, "USE_GCS", None),
        )
