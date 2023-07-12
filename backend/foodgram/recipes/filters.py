from django_filters.rest_framework import FilterSet, filters

from .models import Recipe, Tag


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        method='filter_boolean'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_boolean'
    )

    def filter_boolean(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            field_name = None
            if name == 'is_favorited':
                field_name = 'favorite__user'
            elif name == 'is_in_shopping_cart':
                field_name = 'shopping_list__user'
            if field_name:
                return queryset.filter(**{field_name: user})
        return queryset

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart'
        )
