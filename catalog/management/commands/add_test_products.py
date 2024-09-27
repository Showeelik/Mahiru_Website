from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Удаляет все существующие продукты и категории и добавляет тестовые данные с описанием"

    def handle(self, *args, **kwargs):
        # Удаление всех продуктов и категорий
        self.stdout.write(self.style.WARNING("Удаляем все продукты и категории..."))
        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command("loaddata", "catalog_fixture.json")
        # Вывод успешного сообщения
        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно добавлены с описанием!"))
