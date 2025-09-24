from django.contrib import admin

from catalog.models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Декоратор и класс ProductAdmin настраивают отображение и поведение модели Product в
    административной панели Django."""

    list_display = ("id", "name", "description", "price", "category")
    list_filter = ("category",)
    search_fields = (
        "name",
        "category",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Декоратор и класс CategoryAdmin настраивают отображение и управление моделью
    Category в административной панели Django."""

    list_display = ("id", "name", "description")
    search_fields = ("name",)
