from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.db import models



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

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