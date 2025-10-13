from django.core.validators import FileExtensionValidator
from django.db import models

from users.models import CustomUser


class Category(models.Model):
    """Модель Category хранит информацию о категориях с названием и описанием,
    а также содержит настройки для удобного отображения в административной панели Django.
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Название категории",
    )
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Класс Product — это модель Django, описывающая товар или продукт в базе данных."""

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')

    name = models.CharField(
        max_length=100,
        verbose_name="Название продукта",
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )

    image = models.ImageField(
        upload_to="catalog/media",
        blank=True,
        null=True,
        verbose_name="Изображение",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        help_text="Загрузите изображение в формате JPEG или PNG (макс. 5 МБ)",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    price = models.IntegerField(verbose_name="Цена за единицу", blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('moderated', 'На модерации',),
        ('published', 'Опубликован'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Статус публикации"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "category", "price", "created_at",
                    "updated_at"]
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
            ("can_delete_product", "Can delete product"),
        ]

    def __str__(self):
        return self.name
