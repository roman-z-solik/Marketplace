from django.contrib import admin

from myblogs.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Декоратор и класс BlogAdmin настраивают отображение и поведение модели Blog в
    административной панели Django."""

    verbose_name = "Новое название"
    list_display = ("id", "title", "content", "image", "publication_sign")
    list_filter = ("publication_sign",)
    search_fields = (
        "title",
        "content",
    )
