from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" с нужными правами'

    def handle(self, *args, **kwargs):
        group_name = 'Модератор продуктов'
        group, created = Group.objects.get_or_create(name=group_name)

        product_ct = ContentType.objects.get_for_model(Product)

        delete_permission = Permission.objects.get(codename='delete_product', content_type=product_ct)
        unpublish_permission = Permission.objects.get(codename='can_unpublish_product', content_type=product_ct)

        group.permissions.set([delete_permission, unpublish_permission])

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана и права добавлены.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" уже существует. Права обновлены.'))
