from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Удаляет все существующие продукты и категории и добавляет тестовые данные с описанием'

    def handle(self, *args, **kwargs):
        # Удаление всех продуктов и категорий
        self.stdout.write(self.style.WARNING('Удаляем все продукты и категории...'))
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создание категорий с описанием
        self.stdout.write(self.style.SUCCESS('Добавляем новые категории...'))
        electronics = Category.objects.create(
            name="Electronics",
            description="Категория для всех электронных устройств, таких как компьютеры, смартфоны и т.д."
        )
        books = Category.objects.create(
            name="Books",
            description="Категория для всех видов книг, включая художественную литературу и учебники."
        )
        clothing = Category.objects.create(
            name="Clothing",
            description="Категория для всей одежды и аксессуаров."
        )

        # Создание продуктов с описанием
        self.stdout.write(self.style.SUCCESS('Добавляем новые продукты...'))
        Product.objects.create(
            name="Laptop",
            category=electronics,
            price=999.99,
            description="Мощный ноутбук с 16GB RAM и SSD на 512GB."
        )
        Product.objects.create(
            name="Smartphone",
            category=electronics,
            price=499.99,
            description="Современный смартфон с двойной камерой и 5G поддержкой."
        )
        Product.objects.create(
            name="Fiction Book",
            category=books,
            price=19.99,
            description="Художественная книга о приключениях в параллельных мирах."
        )
        Product.objects.create(
            name="Jacket",
            category=clothing,
            price=59.99,
            description="Удобная куртка для холодной погоды с водоотталкивающей тканью."
        )

        # Вывод успешного сообщения
        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно добавлены с описанием!'))
