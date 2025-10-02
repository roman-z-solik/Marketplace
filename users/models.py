from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта')

    avatar = models.ImageField(
        upload_to='profile_foto',
        blank=True,
        null=True,
        verbose_name="Фото профиля",
        help_text='Загрузите фото профиля',)

    phone = models.CharField(
        max_length=15,
        verbose_name='Телефон',
        blank=True,
        null=True,
        help_text='Введите номер телефона',)

    country = models.CharField(
        max_length=20,
        verbose_name='Страна',
        blank=True,
        null=True,
        help_text='Страна',)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email