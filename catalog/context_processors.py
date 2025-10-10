from .models import Category


def categories_context(request):
    """
    Контекстный процессор для передачи списка всех категорий в каждый шаблон.
    """
    categories = Category.objects.all().order_by('name')
    return {'categories': categories}
