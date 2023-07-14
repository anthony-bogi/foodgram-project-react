from django.contrib import admin

from .models import Favorites, IngredientsInRecipe, Recipe, ShoppingList


class IngredientsAdminInline(admin.TabularInline):
    """Класс для отображения ингредиентов при создании рецепта в админке."""
    model = IngredientsInRecipe
    can_delete = True
    min_num = 1
    extra = 1


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    """Наша модель для рецептов в админке."""
    list_display = (
        'id',
        'name',
        'author',
        'cooking_time',
        'favorites_amount',
    )
    readonly_fields = ('favorites_amount',)
    list_filter = ('name', 'author', 'tags', 'cooking_time',)
    empty_value_display = '--пусто--'
    search_fields = ('name', 'author', 'tags', 'cooking_time',)
    filter_horizontal = ('tags',)
    inlines = (IngredientsAdminInline,)

    @admin.display(description='Количество в избранном')
    def favorites_amount(self, obj):
        return obj.favorite.count()


@admin.register(IngredientsInRecipe)
class AdminIngredients(admin.ModelAdmin):
    """Наша модель для ингредиентов в рецепте в админке."""
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount',
    )
    list_filter = ('recipe', 'ingredient',)
    search_fields = ('recipe', 'ingredient',)


@admin.register(Favorites)
class AdminFavorites(admin.ModelAdmin):
    """Наша модель для избранного в админке."""
    list_display = (
        'id',
        'user',
        'recipe',
    )
    list_filter = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)


@admin.register(ShoppingList)
class AdminShoppingList(admin.ModelAdmin):
    """Наша модель списка покупок в админке."""
    list_display = (
        'id',
        'user',
        'recipe',
    )
    list_filter = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
