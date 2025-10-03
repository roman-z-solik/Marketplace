from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Этот класс представляет собой кастомную форму для создания нового пользователя в Django.
    Он наследуется от встроенного UserCreationForm, который по умолчанию обрабатывает базовые
    поля для регистрации: username, password1 и password2 (пароль и его подтверждение).
    """

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "avatar", "phone", "country")


class CustomUserChangeForm(UserChangeForm):
    """Этот класс представляет собой кастомную форму для изменения данных существующего
    пользователя в Django. Он наследуется от встроенного UserChangeForm, который по умолчанию
    предназначен для редактирования профиля пользователя (включая пароль и другие поля).
    """

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "avatar", "phone", "country")
