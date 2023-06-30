from django.db import models
from django.core.validators import MinValueValidator

from users.models import User
from ingredients.models import Ingredient
from tags.models import Tag


class Recipe(models.Model):
    """Our recipe model."""
    author = models.ForeignKey(
        User,
        verbose_name='автор публикации (пользователь)',
        on_delete=models.CASCADE,
        related_name='recipes',
        help_text='Имя пользователя - автора рецепта'
    )
    name = models.CharField(
        verbose_name='название',
        max_length=200,
        help_text='Название рецепта'
    )
    image = models.ImageField(
        verbose_name='изображение',
        blank=True,
        upload_to='recipes/images',
        help_text='Красивый рисунок к рецепту'
    )
    text = models.TextField(
        verbose_name='текстовое описание',
        help_text='Длинное и подробное описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='ингредиенты',
        through='Ingredients',
        related_name='recipes',
        help_text='Ингредиенты, используемые в рецепте'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='тег',
        related_name='recipes',
        help_text='Тег к рецепту'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='время приготовления в минутах',
        validators=[
            MinValueValidator(1, message='Введите время в минутах >=1.')
        ],
        help_text='Время, затрачиваемое на приготовление блюда в минутах'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def is_favorited(self, user):
        return self.favorites.filter(user=user).exists()

    def is_in_shopping_cart(self, user):
        return self.shopping_list.filter(user=user).exists()

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """Our ingredients in recipe model."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='рецепт',
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
        help_text='Рецепт, в котором используется данный ингредиент'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
        help_text='Название ингредиента'
    )
    amount = models.PositiveIntegerField(
        verbose_name='количество',
        validators=[
            MinValueValidator(1, message='Введите количество >=1.')
        ],
        help_text='Количество указанного ингредиента'
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return f'{self.recipe} - {self.amount} {self.ingredient}'


class Favorites(models.Model):
    """Our favorites of recipes model."""
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
        related_name='favorites',
        help_text='Автор данного рецепта'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='рецепт',
        on_delete=models.CASCADE,
        related_name='favorites',
        help_text='Название рецепта'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
            )
        ]
    
    def __str__(self):
        return f'{self.user} добавил рецепт "{self.recipe}" в Избранное.'


class ShoppingList(models.Model):
    """Our shopping list of recipes model."""
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_list',
        help_text='Автор, кто добавляет рецепт в список покупок'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_list',
        help_text='Название рецепта'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_list'
            )
        ]
    
    def __str__(self):
        return f'{self.user} добавил рецепт "{self.recipe}" в Список своих покупок.'
