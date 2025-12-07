from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title or f"Image {self.pk}"
