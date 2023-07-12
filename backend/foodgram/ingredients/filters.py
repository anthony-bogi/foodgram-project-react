import django_filters

from .models import Ingredient

class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    
    class Meta:
        model = Ingredient
        fields = ['name']

# from django.db.models import Q
# from django.db.models.functions import Lower
# from django_filters.rest_framework import CharFilter, FilterSet

# from .models import Ingredient


# class IngredientFilter(FilterSet):
#     """Наш фильтр для поиска ингредиентов в списке выпадающих имен."""
#     name = CharFilter(method='our_filter_method')

#     def our_filter_method(self, queryset, name, value):
#         if not value:
#             return queryset
#         starts_with_query = Q(name__istartswith=value)
#         contains_query = Q(name__icontains=value)
#         return queryset.annotate(
#             starts_with_match=Lower('name').startswith(Lower(value)),
#             contains_match=Lower('name').contains(Lower(value))
#         ).filter(starts_with_query | contains_query).order_by(
#             '-starts_with_match'
#         )

#     class Meta:
#         model = Ingredient
#         fields = ['name']
