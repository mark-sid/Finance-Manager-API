from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

from .serializers import TransactionSerializer
from .models import Transaction, TransactionStatus
from .analytics import total, by_categories, percentage_by_category
from .filters import TransactionFilter, AnalyticsFilter, filter_by_category
from .schemas import AnalyticsParamsSchema, TransactionParamsSchema


@extend_schema_view(
    list=extend_schema(tags=['api', 'transactions']),
    retrieve=extend_schema(tags=['api', 'transactions']),
    create=extend_schema(tags=['api', 'transactions']),
    update=extend_schema(tags=['api', 'transactions']),
    partial_update=extend_schema(tags=['api', 'transactions']),
    destroy=extend_schema(tags=['api', 'transactions'])
)
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = TransactionFilter # noqa
    pagination_class = PageNumberPagination
    schema = TransactionParamsSchema()


    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(user=user)

        category_id = self.request.GET.get('category_id', None)

        if category_id:
            queryset = filter_by_category(category_id, self.request.user, queryset)

        return queryset


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user

        return context


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class AnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = AnalyticsFilter # noqa
    schema = AnalyticsParamsSchema()


    def get_queryset(self):
        user = self.request.user

        queryset = Transaction.objects.filter(
            user=user,
            status=TransactionStatus.COMPLETED
        )

        category_id = self.request.GET.get('category_id', None)

        if category_id:
            queryset = filter_by_category(category_id, self.request.user, queryset)

        filtered = self.filterset_class(self.request.GET, queryset=queryset)

        return filtered.qs


    def _validate_required_params(self, params_list):
        query_params = self.request.query_params
        missing = [param for param in params_list if not query_params.get(param)]

        if missing:
            raise ValidationError({'Required params': ', '.join(missing)})


    @extend_schema(tags=['api', 'analytics'])
    @action(methods=['GET'], detail=False, url_path='summary')
    def summary(self, request):
        queryset = self.get_queryset()

        data = total(queryset)

        return Response(data=data, status=status.HTTP_200_OK)


    @extend_schema(tags=['api', 'analytics'])
    @action(methods=['GET'], detail=False, url_path='categories')
    def categories(self, request):
        queryset = self.get_queryset()

        data = by_categories(queryset, request.user)

        return Response(data=data, status=status.HTTP_200_OK)


    @extend_schema(tags=['api', 'analytics'])
    @action(methods=['GET'], detail=False, url_path='percentages')
    def percentage_by_category(self, request):
        self._validate_required_params(('type', 'currency'))
        queryset = self.get_queryset()

        data = percentage_by_category(queryset, request.user)

        return Response(data=data, status=status.HTTP_200_OK)
