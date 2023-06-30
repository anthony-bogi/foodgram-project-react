from djoser.serializers import UserCreateSerializer, UserSerializer, PasswordSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.password_validation import validate_password

from .utility import username_is_valid

from .models import User
from recipes.models import Recipe


class OurUserCreateSerializer(UserCreateSerializer):
    """Наш сериализатор для создания/регистрации нового пользователя."""
    class Meta:
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        model = User
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id', },
        }
        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email'],
                message = 'Данные логин или пароль уже используются'
            ),
        )

    def validate_username(self, data):
        if data.lower() == "me":
            raise serializers.ValidationError("me - недопустимое имя пользователя.")
        if not username_is_valid(data):
            raise serializers.ValidationError(
                "Введите корректное имя пользователя."
            )
        return data


class OurUserSerializer(UserSerializer):
    """Наш сериализатор для вывода информации о пользователях."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        model = User

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.subscribers.filter(user=request.user).exists()


class OurPasswordReentrySerializer(serializers.Serializer):
    """Наш сериализатор для смены текущего пароля пользователя."""
    current_password = serializers.CharField(
        max_length=150,
        write_only=True
    )
    new_password = serializers.CharField(
        max_length=150,
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = User


class OurSubscriptionRecipeSerializer(serializers.ModelSerializer):
    """Наш сериализатор для отображения информации о рецепте."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class OurSubscriptionSerializer(UserSerializer):
    """Наш сериализатор для подписки на авторов рецептов."""
    recipes = OurSubscriptionRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'id',
            'email',
            'username',                  
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.subscribers.filter(user=request.user).exists()

    def get_recipes(self, obj):
        max_recipes = self.context['request'].GET.get('recipes_limit')
        if max_recipes:
            recipes = obj.recipes.all()[:int(max_recipes)]
        else:
            recipes = obj.rec.all()
        return OurSubscriptionRecipeSerializer(recipes, many=True).data
