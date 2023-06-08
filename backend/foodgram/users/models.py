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
        unique=True
    )
    username = models.CharField(
        verbose_name='имя пользователя (логин)',
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='фамилия',
        max_length=150,
    )
    password = models.CharField(
        verbose_name='пароль',
        max_length=150
    )
    role = models.CharField(
        verbose_name='пользовательская роль',
        max_length=15,
        choices=CHOICES,
        default='user',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self) -> str:
        return self.username
