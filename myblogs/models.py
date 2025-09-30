from django.db import models


class Blog(models.Model):
    """Модель описывает сущность "Блог"(публикацию) с полями для заголовка, контента,
    изображения, даты создания, флага публикации и счётчика просмотров."""

    title = models.CharField(
        max_length=100, verbose_name="Заголовок", help_text="Введите заголовок"
    )
    content = models.TextField(
        verbose_name="Текст публикации",
        help_text="Введите текст публикации",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="blogs/media",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    publication_sign = models.BooleanField(verbose_name="Опубликовать")
    views_count = models.PositiveIntegerField(
        verbose_name="Количество просмотров", default=0
    )

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"

    def __str__(self):
        return self.title
