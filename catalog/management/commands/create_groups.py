from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группы пользователей с разрешениями для Product'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Product)

        add_perm = Permission.objects.get(codename='add_product', content_type=content_type)
        change_perm = Permission.objects.get(codename='change_product', content_type=content_type)
        delete_perm = Permission.objects.get(codename='delete_product', content_type=content_type)
        view_perm = Permission.objects.get(codename='view_product', content_type=content_type)

        admin_group, created = Group.objects.get_or_create(name='admin')
        admin_group.permissions.set([add_perm, change_perm, delete_perm, view_perm])

        mod_group, created = Group.objects.get_or_create(name='moderator')
        mod_group.permissions.set([change_perm, view_perm])

        user_group, created = Group.objects.get_or_create(name='user')
        user_group.permissions.set([view_perm])

        self.stdout.write(self.style.SUCCESS('Группы созданы успешно'))
