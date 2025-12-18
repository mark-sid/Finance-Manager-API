from .models import Transaction
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import TransactionSerializer, TransactionCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Categories.models import Category
# Create your views here.


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = TransactionCreateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        categories = Category.objects.filter(owner=user)

        total_spend = {}
        expenses_by_category = {}
        transactions_by_category = {}

        for category in categories:
            expenses = {}
            transactions = []
            cat_transactions = category.transactions.all()

            for transaction in cat_transactions:
                currency, amount = transaction.currency, transaction.amount

                if not currency in total_spend:
                    total_spend[currency] = amount
                else:
                    total_spend[currency] += amount

                if not currency in expenses:
                    expenses[currency] = amount
                else:
                    expenses[currency] += amount

                transactions.append(TransactionSerializer(transaction).data)

            cat_name = category.name

            expenses_by_category[cat_name] = expenses
            transactions_by_category[cat_name] = transactions

        return Response(
            {
                'total_spend': total_spend,
                'expenses_by_category': expenses_by_category,
                'transactions_by_category': transactions_by_category
            }, status=status.HTTP_200_OK
        )


