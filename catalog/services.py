from catalog.models import Product
from config.settings import CACHE_ENABLED
from django.core.cache import cache


def get_products_from_cache():
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = 'products_list'
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products


def get_products_by_category(category_id):
    """
    Возвращает список опубликованных продуктов в указанной категории.
    Использует кэш, если включён.
    """
    if not CACHE_ENABLED:
        return Product.objects.filter(category_id=category_id, is_published=True)

    key = f'products_category_{category_id}'
    products = cache.get(key)
    if products is not None:
        return products

    products = Product.objects.filter(category_id=category_id, is_published=True)
    cache.set(key, products)
    return products