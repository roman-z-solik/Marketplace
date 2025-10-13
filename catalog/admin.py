from django.contrib import admin

from catalog.models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'status', 'owner')
    list_filter = ('category', 'status')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Декоратор и класс CategoryAdmin настраивают отображение и управление моделью
    Category в административной панели Django."""

    list_display = ("id", "name", "description")
    search_fields = ("name",)
