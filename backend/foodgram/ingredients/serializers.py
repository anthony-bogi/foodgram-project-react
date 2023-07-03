from rest_framework import serializers

from .models import Ingredient


class OurIngredientSerializer(serializers.ModelSerializer):
    """Наш сериализатор для вывода информации об ингредиентах."""

    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        model = Ingredient
