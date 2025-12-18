from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ['user', 'created_at', 'updated_at']


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ['created_at', 'updated_at']



