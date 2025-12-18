from .models import Category
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import CategorySerializer, CategoryCreateSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(owner=user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = CategoryCreateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)