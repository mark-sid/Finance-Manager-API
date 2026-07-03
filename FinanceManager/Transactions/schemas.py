from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes


ANALYTICS_PARAMS = [
    OpenApiParameter(name='category_id', description='Filter by category', required=False, type=int),
    OpenApiParameter(name='type', description='Filter by type', required=False, type=str),
    OpenApiParameter(name='currency', description='Filter by currency', required=False, type=str),
    OpenApiParameter(name='amount', description='Filter by amount', required=False, type=OpenApiTypes.DECIMAL),
    OpenApiParameter(name='amount__gt', description='Filter by amount greater than', required=False, type=OpenApiTypes.DECIMAL),
    OpenApiParameter(name='amount__lt', description='Filter by amount less than', required=False, type=OpenApiTypes.DECIMAL),
    OpenApiParameter(name='amount__range', description='Filter by amount in range', required=False, type=OpenApiTypes.DECIMAL),
    OpenApiParameter(name='timestamp', description='Filter by timestamp', required=False, type=OpenApiTypes.DATETIME),
    OpenApiParameter(name='timestamp__gt', description='Filter by timestamp greater than', required=False, type=OpenApiTypes.DATETIME),
    OpenApiParameter(name='timestamp__lt', description='Filter by timestamp less than', required=False, type=OpenApiTypes.DATETIME),
    OpenApiParameter(name='timestamp__range', description='Filter by timestamp in range', required=False, type=OpenApiTypes.DATETIME)
]


TRANSACTION_PARAMS = [
    OpenApiParameter(name='status', description='Filter by status', required=False, type=str),
    OpenApiParameter(name='title', description='Filter by title', required=False, type=str),
    OpenApiParameter(name='title_iexact', description='Filter by title iexact', required=False, type=str)
]


class AnalyticsParamsSchema(AutoSchema):
    def get_override_parameters(self):
        params = super().get_override_parameters()

        return params + ANALYTICS_PARAMS


class TransactionParamsSchema(AnalyticsParamsSchema):
    def get_override_parameters(self):
        params = super().get_override_parameters()

        return params + TRANSACTION_PARAMS
