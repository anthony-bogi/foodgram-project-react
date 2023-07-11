from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Subscribe, User
from .utility import username_is_valid


class ModifiedUserCreateSerializer(UserCreateSerializer):
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
                message='Данные логин или пароль уже используются'
            ),
        )

    def validate_username(self, data):
        if data.lower() == "me":
            raise serializers.ValidationError(
                'me - недопустимое имя пользователя.'
            )
        if not username_is_valid(data):
            raise serializers.ValidationError(
                'Введите корректное имя пользователя.'
            )
        return data


class ModifiedUserSerializer(UserSerializer):
    """Наш сериализатор для вывода информации о пользователях."""
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
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


class PasswordReentrySerializer(serializers.Serializer):
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


class SubscriptionRecipeSerializer(serializers.ModelSerializer):
    """Наш сериализатор для отображения информации о рецепте."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionSerializer(ModifiedUserSerializer):
    """Наш сериализатор для подписки на авторов рецептов."""
    recipes = SubscriptionRecipeSerializer(many=True, required=False)
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

    def validate(self, data):
        request = self.context['request']
        author = self.instance
        if request.method == 'DELETE':
            return data
        existing_subscription = Subscribe.objects.filter(
            user=request.user,
            author=author
        )
        if existing_subscription.exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.'
            )
        if author == request.user:
            raise serializers.ValidationError(
                'Невозможно подписаться на самого себя.'
            )
        return data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.subscribers.filter(user=request.user).exists()

    def get_recipes(self, obj):
        max_recipes = self.context['request'].GET.get('recipes_limit')
        queryset = obj.recipes.all()
        if max_recipes:
            max_recipes = int(max_recipes)
            queryset = queryset[:max_recipes]
        return SubscriptionRecipeSerializer(queryset, many=True).data
