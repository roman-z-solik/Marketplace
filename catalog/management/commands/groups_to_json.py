from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product
import json


class Command(BaseCommand):
    help = 'Выгружает существующие группы пользователей с разрешениями для Product в JSON'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Product)

        groups = Group.objects.all()

        groups_data = []
        for group in groups:
            permissions_data = []
            for perm in group.permissions.all():
                if perm.content_type == content_type:
                    permissions_data.append({
                        'codename': perm.codename,
                        'name': perm.name,
                        'content_type': perm.content_type.model,
                    })
            groups_data.append({
                'name': group.name,
                'permissions': permissions_data,
            })

        json_output = json.dumps(groups_data, ensure_ascii=False, indent=4)
        self.stdout.write(json_output)
