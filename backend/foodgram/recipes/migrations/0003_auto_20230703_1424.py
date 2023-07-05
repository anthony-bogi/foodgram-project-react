# Generated by Django 3.2.19 on 2023-07-03 11:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_auto_20230627_1528'),
        ('ingredients', '0003_alter_ingredient_options'),
        ('recipes', '0002_auto_20230627_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(help_text='Время, необходимое для приготовления блюда в минутах', validators=[django.core.validators.MinValueValidator(1, message='Введите время в минутах >=1.')], verbose_name='время приготовления в минутах'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, help_text='Красивый рисунок, иллюстрирующий рецепт', upload_to='recipes/images', verbose_name='изображение'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Список продуктов (ингредиентов), используемых в блюде', related_name='recipes', through='recipes.Ingredients', to='ingredients.Ingredient', verbose_name='ингредиенты'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(help_text='Название блюда', max_length=200, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(help_text='Тег/теги к рецепту', related_name='recipes', to='tags.Tag', verbose_name='теги'),
        ),
    ]
