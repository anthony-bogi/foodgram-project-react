from django.contrib import admin

from .models import Recipe, Ingredients, Ingredient, Tag, Favorites, ShoppingList


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


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    """Our model for ingredient in the admin panel."""
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    """Our model for tag in the admin panel."""
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    list_filter = ('name', 'slug',)
    search_fields = ('name', 'slug',)


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
