from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    # list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
    # list_filter = ['is_staff', 'is_active']
    # fieldsets = UserAdmin.fieldsets + (
    #     (None, {'fields': ('avatar', 'phone_number', 'country')}),
    # )
    # add_fieldsets = UserAdmin.add_fieldsets + (
    #     (None, {'fields': ('avatar', 'phone_number', 'country')}),
    # )
    search_fields = ['email']
    ordering = ['email']