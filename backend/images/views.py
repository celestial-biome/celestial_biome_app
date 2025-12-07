from rest_framework import viewsets, permissions

from .models import Image
from .serializers import ImageSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
