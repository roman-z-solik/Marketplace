from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product
import json
import os


class Command(BaseCommand):
    help = 'Загружает группы пользователей с разрешениями для Product из JSON-файла'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            type=str,
            default='groups.json',
            help='Путь к JSON-файлу с группами (по умолчанию: groups.json)',
        )

    def handle(self, *args, **options):
        json_file_path = options['json_file']

        if not os.path.exists(json_file_path):
            raise CommandError(f'Файл {json_file_path} не найден.')

        with open(json_file_path, 'r', encoding='utf-8') as f:
            try:
                groups_data = json.load(f)
            except json.JSONDecodeError as e:
                raise CommandError(f'Ошибка парсинга JSON: {e}')

        content_type = ContentType.objects.get_for_model(Product)

        for group_data in groups_data:
            group_name = group_data.get('name')
            if not group_name:
                self.stdout.write(self.style.WARNING(f'Пропущена группа без имени: {group_data}'))
                continue

            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'Создана группа: {group_name}')
            else:
                self.stdout.write(f'Обновлена группа: {group_name}')

            permissions = []
            for perm_data in group_data.get('permissions', []):
                codename = perm_data.get('codename')
                if not codename:
                    self.stdout.write(
                        self.style.WARNING(f'Пропущено разрешение без codename в группе {group_name}: {perm_data}'))
                    continue

                try:
                    perm = Permission.objects.get(codename=codename, content_type=content_type)
                    permissions.append(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'Разрешение {codename} для модели Product не найдено, пропущено.'))

            group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS('Загрузка групп из JSON завершена успешно.'))
