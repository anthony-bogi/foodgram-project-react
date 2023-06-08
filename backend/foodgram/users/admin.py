from django.contrib import admin

from .models import User

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    """Our model for users in the admin panel."""
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
