from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import CategorySerializer
from .models import Category


@extend_schema_view(
    list=extend_schema(tags=['api', 'categories']),
    retrieve=extend_schema(tags=['api', 'categories']),
    create=extend_schema(tags=['api', 'categories']),
    update=extend_schema(tags=['api', 'categories']),
    partial_update=extend_schema(tags=['api', 'categories']),
    destroy=extend_schema(tags=['api', 'categories'])
)
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Category.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)
