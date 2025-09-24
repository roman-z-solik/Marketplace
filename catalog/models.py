from django.db import models


class Category(models.Model):
    """Модель Category хранит информацию о категориях с названием и описанием,
    а также содержит настройки для удобного отображения в административной панели Django.
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Название категории",
        help_text="Введите название категории",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание", blank=True, null=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Класс Product — это модель Django, описывающая товар или продукт в базе данных."""

    name = models.CharField(
        max_length=100, verbose_name="Название продукта", help_text="Название продукта"
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Описание продукта", blank=True, null=True
    )
    image = models.ImageField(
        upload_to="catalog/media",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Изображение товара",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
        help_text="Выберите категорию",
    )
    price = models.IntegerField(
        verbose_name="Цена за единицу", help_text="Введите цену", blank=True, null=True
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "category", "price", "created_at", "updated_at"]

    def __str__(self):
        return self.name
