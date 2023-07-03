from rest_framework import serializers

from .models import Tag


class OurTagSerializer(serializers.ModelSerializer):
    """Наш сериализатор для вывода информации о тегах."""

    class Meta:
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
        model = Tag
