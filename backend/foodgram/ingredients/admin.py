from django.contrib import admin

from .models import Ingredient


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    """Наша модель для ингредиента в админке."""
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    search_fields = ('name',)
