from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Наша расширенная модель работы с пользователями."""
    CHOICES = (
        ('user', 'user'),
        ('admin', 'admin'),
    )
    email = models.EmailField(
        verbose_name='адрес электронной почты (email)',
        max_length=254,
        unique=True,
        help_text=(
            'Электронный адрес, '
            'с которым будет связана учетная запись пользователя'
        )
    )
    username = models.CharField(
        verbose_name='имя пользователя (логин)',
        max_length=150,
        unique=True,
        help_text=(
            'Имя пользователя, '
            'под которым будут видны рецепты и комментарии'
        )
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
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username


class Subscribe(models.Model):
    """Наша модель для подписки на пользователя."""
    id = models.AutoField(
        primary_key=True,
        verbose_name="ID",
        help_text='Уникальный идентификатор ID'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name="Подписчик",
        help_text='Имя пользователя, кто подписывается'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name="Автор",
        help_text='Имя пользователя, на кого подписываются'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата подписки",
        help_text='Дата и время подписки'
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe'
            )
        ]

    def __str__(self):
        return f'{self.user.email} подписан на {self.author.email}'
