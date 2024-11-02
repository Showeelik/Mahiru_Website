from django.core.cache import cache
from .models import Product


class ProductService:
    @classmethod
    def get_products(cls) -> list[Product]:
        """
        Возвращает список всех продуктов.

        Returns:
            list[Product]: список продуктов
        """
        return Product.objects.all()

    @classmethod
    def get_product_by_id(cls, product_id) -> Product:
        """
        Возвращает продукт по ID.

        Args:
            product_id (int): ID продукта

        Returns:
            Product: продукт
        """
        return Product.objects.get(id=product_id)

    @classmethod
    def get_published_products(cls) -> list[Product]:
        """
        Возвращает список продуктов с публикацией.

        Returns:
            list[Product]: список продуктов
        """
        return Product.objects.filter(is_published=True)

    @classmethod
    def get_product_by_name(cls, product_name) -> Product:
        """
        Возвращает продукт по имени.

        Args:
            product_name (str): Имя продукта

        Returns:
            Product: продукт
        """
        return Product.objects.get(name=product_name)

    @classmethod
    def get_published_products_by_name(cls, product_name) -> list[Product]:
        """
        Возвращает список продуктов по имени.

        Args:
            product_name (str): Имя продукта

        Returns:
            list[Product]: список продуктов
        """
        return Product.objects.filter(name=product_name, is_published=True)

    @classmethod
    def get_published_products_by_category(cls, category_id) -> list[Product]:
        """
        Возвращает список продуктов в указанной категории.
        Использует кэш для оптимизации.

        Args:
            category_id (int): ID категории

        Returns:
            list[Product]: список продуктов
        """
        cache_key = f"products_in_category_{category_id}"
        products = cache.get(cache_key)

        if products is None:
            products = list(Product.objects.filter(category_id=category_id, is_published=True))
            cache.set(cache_key, products, 60 * 15)  # Кэшируем на 15 минут

        return products

    @classmethod
    def get_published_products_by_category_name(cls, category_name) -> list[Product]:
        """
        Возвращает список продуктов в указанной категории по имени.

        Args:
            category_name (str): Имя категории

        Returns:
            list[Product]: список продуктов
        """
        return Product.objects.filter(category__name=category_name, is_published=True)