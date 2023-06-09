from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Our extended model of work with users."""
    CHOICES = (
        ('user', 'user'),
        ('admin', 'admin'),
    )
    email = models.EmailField(
        verbose_name='адрес электронной почты (email)',
        max_length=254,
        unique=True,
        help_text='Электронный адрес, с которым будет связана учетная запись пользователя'
    )
    username = models.CharField(
        verbose_name='имя пользователя (логин)',
        max_length=150,
        unique=True,
        help_text='Имя пользователя, под которым будут видны рецепты и комментарии'
    )
    first_name = models.CharField(
        verbose_name='имя',
        max_length=150,
        help_text='Имя пользователя'
    )
    last_name = models.CharField(
        verbose_name='фамилия',
        max_length=150,
        help_text='Фамилия пользователя'
    )
    password = models.CharField(
        verbose_name='пароль',
        max_length=150,
        help_text='Пароль от учетной записи'
    )
    role = models.CharField(
        verbose_name='пользовательская роль',
        max_length=15,
        choices=CHOICES,
        default='user',
        blank=True,
        null=True,
        help_text='Роль зарегистрированного пользователя'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self) -> str:
        return self.username
