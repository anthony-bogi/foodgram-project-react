# Generated by Django 3.2.19 on 2023-06-27 12:28

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ingredients', '0002_auto_20230627_1528'),
        ('tags', '0002_auto_20230627_1528'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorites',
            name='recipe',
            field=models.ForeignKey(help_text='Название рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipes.recipe', verbose_name='рецепт'),
        ),
        migrations.AlterField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(help_text='Автор данного рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='amount',
            field=models.PositiveIntegerField(help_text='Количество указанного ингредиента', validators=[django.core.validators.MinValueValidator(1, message='Введите количество >=1.')], verbose_name='количество'),
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='ingredient',
            field=models.ForeignKey(help_text='Название ингредиента', on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_in_recipe', to='ingredients.ingredient', verbose_name='ингредиент'),
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='recipe',
            field=models.ForeignKey(help_text='Рецепт, в котором используется данный ингредиент', on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_in_recipe', to='recipes.recipe', verbose_name='рецепт'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(help_text='Имя пользователя - автора рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='автор публикации (пользователь)'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(help_text='Время, затрачиваемое на приготовление блюда в минутах', validators=[django.core.validators.MinValueValidator(1, message='Введите время в минутах >=1.')], verbose_name='время приготовления в минутах'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, help_text='Красивый рисунок к рецепту', upload_to='recipes/images', verbose_name='изображение'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Ингредиенты, используемые в рецепте', related_name='recipes', through='recipes.Ingredients', to='ingredients.Ingredient', verbose_name='ингредиенты'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(help_text='Название рецепта', max_length=200, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(help_text='Тег к рецепту', related_name='recipes', to='tags.Tag', verbose_name='тег'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(help_text='Длинное и подробное описание рецепта', verbose_name='текстовое описание'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='recipe',
            field=models.ForeignKey(help_text='Название рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list', to='recipes.recipe', verbose_name='рецепт'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='user',
            field=models.ForeignKey(help_text='Автор, кто добавляет рецепт в список покупок', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
