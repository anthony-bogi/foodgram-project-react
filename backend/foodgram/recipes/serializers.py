from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from ingredients.models import Ingredient
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import ModifiedUserSerializer

from .constants import (AMOUNT_INGREDIENT_MAX_VALUE,
                        AMOUNT_INGREDIENT_MIN_VALUE, COOKING_TIME_MAX_VALUE,
                        COOKING_TIME_MIN_VALUE)
from .models import IngredientsInRecipe, Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Наш сериализатор для отображения списка рецептов."""
    author = ModifiedUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
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
    cooking_time = serializers.IntegerField()

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
        return recipe.ingredients.annotate(
            amount=F('ingredients_in_recipe__amount')
        ).values(
            'id',
            'name',
            'measurement_unit',
            'amount',
        )

    def get_is_favorited(self, obj):
        request = self.context['request']
        if not request or request.user.is_anonymous:
            return False
        user = request.user
        return user.favorite.filter(recipe_id=obj.pk).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        if not request or request.user.is_anonymous:
            return False
        user = request.user
        return user.shopping_list.filter(recipe_id=obj.pk).exists()


class IngredientsInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели IngredientsInRecipe."""

    class Meta:
        model = IngredientsInRecipe
        fields = (
            'id',
            'amount',
            'ingredient',
        )


class IngredientForCreateSerializer(serializers.ModelSerializer):
    """Наш сериализатор для ингредиентов при создании рецепта."""
    ingredients_in_recipe = IngredientsInRecipeSerializer(many=True)

    class Meta:
        fields = (
            'id',
            'ingredients_in_recipe',
        )
        model = Ingredient


class RecipeCreateUpdateSerializer(RecipeSerializer):
    """Наш сериализатор для создания/обновления рецепта."""
    ingredients = IngredientForCreateSerializer(
        many=True,
        read_only=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    cooking_time = serializers.IntegerField(
        min_value=COOKING_TIME_MIN_VALUE,
        max_value=COOKING_TIME_MAX_VALUE,
        error_messages={'min_value':
                        ' Время приготовления должно быть >= 1.',
                        'max_value':
                        ' Время приготовления должно быть <= 32000.'}
    )

    def process_ingredients(self, recipe, ingredients_data):
        ingredient_ids = [
            ingredient_data.get('id') for ingredient_data in ingredients_data
        ]
        ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
        bulk_create_data = []
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            amount = ingredient_data.get('amount')
            try:
                ingredient = ingredients.get(id=ingredient_id)
            except ObjectDoesNotExist:
                continue
            bulk_create_data.append(
                IngredientsInRecipe(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=amount
                )
            )
        with transaction.atomic():
            IngredientsInRecipe.objects.bulk_create(bulk_create_data)

    def create(self, validated_data):
        author = self.context['request'].user
        validated_data['author'] = author
        ingredients_data = self.context['request'].data.get('ingredients', [])
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.process_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, recipe, validated_data):
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.image = validated_data.get('image', recipe.image)
        recipe.cooking_time = validated_data.get(
            'cooking_time',
            recipe.cooking_time
        )
        ingredients_data = self.context['request'].data.get('ingredients', [])
        IngredientsInRecipe.objects.filter(recipe=recipe).delete()
        self.process_ingredients(recipe, ingredients_data)
        tags_data = validated_data.get('tags', [])
        recipe.tags.clear()
        tag_serializer = serializers.SlugRelatedField(
            many=True, slug_field='name', queryset=Tag.objects.all()
        )
        tags = tag_serializer.to_internal_value(tags_data)
        recipe.tags.set(tags)
        recipe.save()
        return recipe

    def validate(self, data):
        ingredients_data = self.context['request'].data.get('ingredients', [])
        for ingredient_data in ingredients_data:
            amount = ingredient_data.get('amount')
            if not (AMOUNT_INGREDIENT_MIN_VALUE < amount <
                    AMOUNT_INGREDIENT_MAX_VALUE):
                raise serializers.ValidationError({
                    'amount': 'Введите количесвто между 1 и 50000.'
                })

        ingredient_ids = [
            ingredient_data.get('id') for ingredient_data in ingredients_data
        ]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError({
                'ingredients':
                ' Нельзя добавлять повторно один и тот же ингредиент.'
            })

        return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        tags = instance.tags.all()
        tag_serializer = TagSerializer(tags, many=True)
        ret['tags'] = tag_serializer.data
        ingredients = instance.ingredients.annotate(
            amount=F('ingredients_in_recipe__amount')
        ).values(
            'id',
            'name',
            'measurement_unit',
            'amount',
        )
        ret['ingredients'] = ingredients
        return ret


class FavoritesSLRecipeSerializer(serializers.ModelSerializer):
    """
    Наш сериализатор для отображения рецепта в избранном и списке покупок.
    """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
