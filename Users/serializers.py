from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserPasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=50, required=True)
    new_password = serializers.CharField(max_length=50, required=True)

    def update(self, instance, validated_data):
        user = instance

        if not user.check_password(validated_data['old_password']):
            raise serializers.ValidationError({"old_password": "Invalid user old password"})


        user.set_password(validated_data['new_password'])
        user.save()

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

