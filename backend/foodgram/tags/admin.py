from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    """Our model for tag in the admin panel."""
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    list_filter = ('name', 'slug',)
    search_fields = ('name', 'slug',)
