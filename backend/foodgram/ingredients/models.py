from django.db import models


class Ingredient(models.Model):
    """Our ingredient model."""
    name = models.CharField(
        verbose_name='название',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='единица измерения',
        max_length=200
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'
