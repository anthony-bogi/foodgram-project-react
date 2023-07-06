from django.db import models


class Ingredient(models.Model):
    """Наша модель ингредиентов."""
    name = models.CharField(
        verbose_name='название',
        max_length=200,
        help_text='Название ингредиента',
    )
    measurement_unit = models.CharField(
        verbose_name='единица измерения',
        max_length=200,
        help_text='Единица измерения данного ингредиента',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'
