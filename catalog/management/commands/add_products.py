from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    """Данный класс Command представляет собой пользовательскую команду Django, предназначенную
    для добавления (или обновления) набора продуктов в базу данных."""

    help = "Добавление продукта в базу данных"

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Category.objects.all().delete()

        category, _ = Category.objects.get_or_create(
            name="Смартфоны", description="Лучшие смартфоны по доступным ценам"
        )

        phones = [
            {
                "name": "Iphone 15",
                "description": "512GB, Gray space",
                "price": 210000,
                "catalog": category,
            },
            {
                "name": "Samsung Galaxy C23 Ultra",
                "description": "256GB, Серый цвет, 200MP камера",
                "price": 180000,
                "catalog": category,
            },
            {
                "name": "Xiaomi Redmi Note 11",
                "description": "1024GB, Синий",
                "price": 31000,
                "catalog": category,
            },
        ]

        for phone_data in phones:
            phone, created = Product.objects.get_or_create(**phone_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Позиция добавлена: {phone.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Позиция уже существует: {phone.name}")
                )
