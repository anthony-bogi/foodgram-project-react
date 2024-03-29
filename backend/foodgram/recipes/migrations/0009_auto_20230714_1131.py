# Generated by Django 3.2.19 on 2023-07-14 08:31

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0005_remove_ingredient_amount'),
        ('recipes', '0008_auto_20230709_1752'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientsInRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(help_text='Количество указанного ингредиента', validators=[django.core.validators.MinValueValidator(1, message='Введите количество >=1.'), django.core.validators.MaxValueValidator(32000, message='Введите количество <= 32000.')], verbose_name='количество')),
                ('ingredient', models.ForeignKey(help_text='Название ингредиента', on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_in_recipe', to='ingredients.ingredient', verbose_name='ингредиент')),
                ('recipe', models.ForeignKey(help_text='Рецепт, в котором используется данный ингредиент', on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_in_recipe', to='recipes.recipe', verbose_name='рецепт')),
            ],
            options={
                'verbose_name': 'Ингредиент в рецепте',
                'verbose_name_plural': 'Ингредиенты в рецептах',
                'ordering': ('id',),
            },
        ),
        migrations.DeleteModel(
            name='Ingredients',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Список продуктов (ингредиентов), используемых в блюде', related_name='recipes', through='recipes.IngredientsInRecipe', to='ingredients.Ingredient', verbose_name='ингредиенты'),
        ),
    ]
