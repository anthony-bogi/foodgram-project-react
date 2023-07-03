from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    """Наша модель для тега в админке."""
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    list_filter = ('name', 'slug',)
    search_fields = ('name', 'slug',)
