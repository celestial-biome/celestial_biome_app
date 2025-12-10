# backend/images/models.py

from django.contrib.auth.models import User
from django.db import models

from .storage import get_image_storage


class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    title = models.CharField(max_length=255, blank=True)

    # ★ここで storage を明示的に指定
    image = models.ImageField(
        storage=get_image_storage(),  # ← ここがポイント
        upload_to="images/",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Image {self.id}"
