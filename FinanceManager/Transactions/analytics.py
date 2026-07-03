from django.db.models import Sum, Q, Value
from django.db.models.functions import Coalesce
from collections import defaultdict



def total(queryset):
    result = queryset.aggregate(
        total=Sum('amount')
    )

    return result


def by_categories(queryset, user):
    queryset = queryset.filter(
        category__owner=user
    ).values('currency', 'category__name').annotate(
        total=Sum('amount')
    )

    result = defaultdict(dict)

    for item in queryset:
        category_name = item['category__name']
        currency = item['currency']

        result[category_name][currency] = item['total']

    return result


def percentage_by_category(queryset, user):
    total_sum = total(queryset)['total']

    queryset = queryset.values(
        category_name=Coalesce('category__name', Value('Other'))
    ).annotate(
        Sum('amount'),
        filter=Q(category__owner=user)
    )

    result = defaultdict(float)

    for item in queryset:
        result[item['category_name']] = round(
            item['amount__sum'] / total_sum * 100, 2
        )

    return result