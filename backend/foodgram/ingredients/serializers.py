from rest_framework import serializers

from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Наш сериализатор для вывода информации об ингредиентах."""

    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        model = Ingredient


class IngredientForCreateSerializer(serializers.ModelSerializer):
    """Наш сериализатор для ингредиентов при создании рецепта."""

    class Meta:
        fields = (
            'id',
        )
        model = Ingredient
