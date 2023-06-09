from django.contrib import admin

from .models import Recipe, Ingredients, Favorites, ShoppingList


class IngredientsAdminInline(admin.TabularInline):
    """Class for displaying ingredients when creating a recipe in the admin panel."""
    model = Ingredients
    can_delete = True
    extra = 1


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    """Our model for recipes in the admin panel."""
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
        return obj.favorites.count()


@admin.register(Ingredients)
class AdminIngredients(admin.ModelAdmin):
    """Our model for ingredients in recipe in the admin panel."""
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
    """Our model for favorites in the admin panel."""
    list_display = (
        'id',
        'user',
        'recipe',
    )
    list_filter = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)


@admin.register(ShoppingList)
class AdminShoppingList(admin.ModelAdmin):
    """Our model for shopping list in the admin panel."""
    list_display = (
        'id',
        'user',
        'recipe',
    )
    list_filter = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
