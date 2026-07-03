from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def validate_category(self, value):
        if value is None:
            return None

        user = self.context.get('user')

        if value.owner != user:
            raise serializers.ValidationError('Access to category denied')

        return value
