from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters

from .models import Transaction
from Categories.models import Category


class AnalyticsFilter(filters.FilterSet):
    type = filters.CharFilter(field_name='type', method='filter_text_choices')
    currency = filters.CharFilter(field_name='currency', method='filter_currency')

    def filter_text_choices(self, queryset, name, value):
        return queryset.filter(**{name: value.capitalize()})

    def filter_currency(self, queryset, name, value):
        return queryset.filter(**{name: value.upper()})

    class Meta:
        model = Transaction
        fields = {
            'amount': ['exact', 'gt', 'lt', 'range'],
            'timestamp': ['exact', 'gt', 'lt', 'range'],
        }


class TransactionFilter(AnalyticsFilter):
    status = filters.CharFilter(field_name='status', method='filter_text_choices')

    class Meta:
        model = Transaction
        fields = {
            'title': ['iexact', 'icontains'],
            'amount': ['exact', 'gt', 'lt', 'range'],
            'timestamp': ['exact', 'gt', 'lt', 'range'],
        }


def filter_by_category(category_id, user, queryset):
    category = get_object_or_404(Category, id=category_id)

    if category.owner != user:
        raise PermissionDenied(
            detail="Access to category denied" # noqa
        )

    queryset = queryset.filter(category=category)

    return queryset
