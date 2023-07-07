from django.contrib import admin

from .models import Subscribe, User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    """Наша модель для пользователей в админке."""
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
    )
    list_filter = ('email', 'username',)
    empty_value_display = '--пусто--'
    search_fields = ('username', 'email', 'first_name', 'last_name',)


@admin.register(Subscribe)
class AdminSubscribe(admin.ModelAdmin):
    """Наша модель для подписок в админке."""
    list_display = (
        'id',
        'user',
        'author',
        'created_at',
    )
    list_filter = ('user',)
    empty_value_display = '--пусто--'
    search_fields = ('user',)
