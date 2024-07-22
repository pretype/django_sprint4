"""Модуль для регистрации моделей в админ-панели."""

from django.contrib import admin

from .models import Category, Comment, Location, Post


class PostAdmin(admin.ModelAdmin):
    """Класс для указания полей модели Post, отображаемых в админ-панели."""

    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category'
    )


class CategoryAdmin(admin.ModelAdmin):
    """Класс для указания полей модели Category, отображаемых в админке."""

    list_display = (
        'title',
        'description',
        'slug'
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location)
admin.site.register(Comment)
