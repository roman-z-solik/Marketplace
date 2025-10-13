from django.core.cache import cache
from catalog.models import Product, Category


def get_products_by_category(category_id, user=None):
    """
    Сервисная функция для получения всех продуктов в указанной категории
    с поддержкой кеширования и проверки прав доступа
    """
    cache_key = f'category_{category_id}_products'
    if user and user.is_staff:
        cache_key = f'category_{category_id}_products_staff'
    products = cache.get(cache_key)
    if products is None:
        products = Product.objects.filter(
            category_id=category_id
        ).select_related('category', 'owner')

        products = list(products)
        cache.set(cache_key, products, 60 * 15)
        if user and not user.is_staff:
            products = [p for p in products if p.status == 'published']
    return products


def get_category_with_stats(category_id, user=None):
    """
    Получение категории со статистикой продуктов
    """
    cache_key = f'category_{category_id}_stats'
    category_data = cache.get(cache_key)
    if category_data is None:
        try:
            category = Category.objects.get(pk=category_id)
            total_products = Product.objects.filter(pk=category_id).count()
            published_products = Product.objects.filter(
                category_id=category_id,
                status='published'
            ).count()
            category_data = {
                'category': category,
                'total_products': total_products,
                'published_products': published_products,
                'draft_products': total_products - published_products,
            }
            cache.set(cache_key, category_data, 60 * 15)
        except Category.DoesNotExist:
            return None
    return category_data


def clear_category_cache(category_id):
    """
    Очистка кеша категории
    """
    cache_keys = [
        f'category_{category_id}_products',
        f'category_{category_id}_products_staff',
        f'category_{category_id}_stats',
    ]
    for key in cache_keys:
        cache.delete(key)


def get_cached_products(user=None):
    """
    Сервисная функция для получения кешированного списка продуктов
    """
    cache_key = 'all_products'
    if user and user.is_staff:
        cache_key = 'all_products_staff'

    products = cache.get(cache_key)

    if products is None:
        products = list(Product.objects.select_related('category', 'owner').all())
        cache.set(cache_key, products, 60 * 15)

    if user and not user.is_staff:
        products = [p for p in products if p.status == 'published']
    return products


def get_cached_categories():
    """
    Сервисная функция для получения кешированного списка категорий
    """
    cache_key = 'all_categories'
    categories = cache.get(cache_key)

    if categories is None:
        categories = list(Category.objects.all())
        cache.set(cache_key, categories, 60 * 30)  # 30 минут

    return categories


def clear_products_cache():
    """
    Очистка всего кеша продуктов
    """
    cache_keys = ['all_products', 'all_products_staff', 'all_categories']

    for key in cache_keys:
        cache.delete(key)

    for key in list(cache.keys('category_products_*')):
        cache.delete(key)


def clear_category_cache(category_id):
    """
    Очистка кеша конкретной категории
    """
    cache_keys = [
        f'category_products_{category_id}',
        f'category_full_{category_id}',
    ]

    for key in cache_keys:
        cache.delete(key)
