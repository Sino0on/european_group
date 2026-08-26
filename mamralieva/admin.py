from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(TranslationAdmin):
    list_display = ('title', 'post_type', 'published_at', 'is_active')
    list_editable = ('is_active',)
    list_display_links = ('title',)
    list_filter = ('post_type', 'is_active')
    date_hierarchy = 'published_at'
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Тип записи', {
            'fields': ('post_type',),
        }),
        ('Основное', {
            'fields': ('title', 'slug', 'cover_image', 'excerpt'),
        }),
        ('Статья на сайте', {
            'fields': ('content',),
            'description': 'Заполняется только для типа "Статья на сайте".',
        }),
        ('Внешняя ссылка', {
            'fields': ('external_url',),
            'description': 'Заполняется только для типа "Внешняя ссылка" — сюда попадёт читатель по кнопке "Подробнее".',
        }),
        ('Публикация', {
            'fields': ('published_at', 'order', 'is_active'),
        }),
    )
