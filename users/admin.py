from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Декоратор и класс CustomUserAdmin настраивают отображение и поведение модели User в
    административной панели Django."""

    verbose_name = "Новый пользователь"
    list_display = ("email", "username", "id", "is_staff", "is_active")
    search_fields = (
        "email",
        "is_staff",
        "is_active",
    )
