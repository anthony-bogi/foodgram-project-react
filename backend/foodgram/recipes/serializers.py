from rest_framework import serializers
from django.db.models import F
from drf_extra_fields.fields import Base64ImageField

from recipes.models import Recipe, Ingredients
from ingredients.models import Ingredient
from tags.models import Tag
from users.models import User

from ingredients.serializers import OurIngredientSerializer
from tags.serializers import OurTagSerializer
from users.serializers import OurUserSerializer


class OurRecipeSerializer(serializers.ModelSerializer):
    """Наш сериализатор для отображения списка рецептов."""
    author = OurUserSerializer()
    ingredients = serializers.SerializerMethodField()
    tags = OurTagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        model = Recipe

    def get_ingredients(self, obj):
        recipe = obj
        ingredients = recipe.ingredients.annotate(
            amount=F('ingredients_in_recipe__amount')
        ).values(
            'id',
            'name',
            'measurement_unit',
            'amount',
        )
        return ingredients

    def get_is_favorited(self, obj):
        request = self.context['request']
        if not request or request.user.is_anonymous:
            return False
        return obj.is_favorited(request.user)
        
    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        if not request or request.user.is_anonymous:
            return False
        return obj.is_in_shopping_cart(request.user)


class OurRecipeCreateSerializer(serializers.ModelSerializer):
    """Наш сериализатор для создания рецепта. Вводные данные."""
    ingredients = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True,
        allow_null=True,
        required=False
    )
    name = serializers.CharField(
        max_length=200
    )
    text = serializers.CharField()
    cooking_time = serializers.IntegerField(
        min_value=1,
        error_messages={'min_value': 'Время приготовления должно быть больше или равно 1.'}
    )

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        recipe = obj
        ingredients = recipe.ingredients.annotate(
            amount=F('ingredients_in_recipe__amount')
        ).values(
            'id',
            'amount',
        )
        return ingredients
    

class OurRecipeCreateOutputSerializer(serializers.ModelSerializer):
    """Наш сериализатор для создания рецепта. Выходные данные."""
    id = serializers.IntegerField(
        read_only=True
    )
    tags = OurTagSerializer(
        many=True
    )
    author = author = OurUserSerializer(
        default=serializers.CurrentUserDefault()
    )
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    name = serializers.CharField(
        max_length=200
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True,
        allow_null=True,
        required=False
    )    
    text = serializers.CharField()
    cooking_time = serializers.IntegerField(
        min_value=1,
        error_messages={'min_value': 'Время приготовления должно быть больше или равно 1.'}
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        recipe = obj
        ingredients = recipe.ingredients.annotate(
            amount=F('ingredients_in_recipe__amount')
        ).values(
            'id',
            'name',
            'measurement_unit',
            'amount',
        )
        return ingredients

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.is_favorited(user)

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.is_in_shopping_cart(user)


class OurFavoritesSLRecipeSerializer(serializers.ModelSerializer):
    """Наш сериализатор для отображения рецепта в избранном и списке покупок."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
