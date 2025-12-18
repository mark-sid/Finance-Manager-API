from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserPasswordUpdateSerializer,
)


# Create your views here.


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        serializer = UserSerializer(instance=user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserSerializer(instance=user, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user

        serializer = UserPasswordUpdateSerializer(instance=user, data=request.data)

        if serializer.is_valid():
            response_data = serializer.update(user, serializer.validated_data)

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.delete()

        return Response({}, status=status.HTTP_200_OK)





