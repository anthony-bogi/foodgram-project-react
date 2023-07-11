from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from ingredients.models import Ingredient
from ingredients.serializers import IngredientForCreateSerializer
from recipes.constants import COOKING_TIME_MAX_VALUE, COOKING_TIME_MIN_VALUE
from recipes.models import Ingredients, Recipe
from rest_framework import serializers
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import ModifiedUserSerializer


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

    def create(self, validated_data):
        author = self.context['request'].user
        validated_data['author'] = author
        ingredients_data = self.context['request'].data.get('ingredients', [])
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        ingredients = []
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
                Ingredients(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=amount
                )
            )
        with transaction.atomic():
            Ingredients.objects.bulk_create(bulk_create_data)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        ingredients_data = self.context['request'].data.get('ingredients', [])
        Ingredients.objects.filter(recipe=instance).delete()
        ingredients = []
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
                Ingredients(
                    recipe=instance,
                    ingredient=ingredient,
                    amount=amount
                )
            )
        with transaction.atomic():
            Ingredients.objects.bulk_create(bulk_create_data)
        tags_data = validated_data.get('tags', [])
        instance.tags.clear()
        tag_serializer = serializers.SlugRelatedField(
            many=True, slug_field='name', queryset=Tag.objects.all()
        )
        tags = tag_serializer.to_internal_value(tags_data)
        instance.tags.set(tags)
        instance.save()
        return instance

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
