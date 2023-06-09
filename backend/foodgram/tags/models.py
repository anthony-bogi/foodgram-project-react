from django.db import models
from django.core.validators import RegexValidator


class Tag(models.Model):
    """Our tag model."""
    name = models.CharField(
        verbose_name='название',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='цвет в HEX',
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Введите значение в формате HEX'
            )
        ],
        default='#ffffff'
    )
    slug = models.SlugField(
        verbose_name='уникальный слаг',
        max_length=200,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[-a-zA-Z0-9_]+$',
                message='Введите уникальный слаг'
            )
        ]
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
