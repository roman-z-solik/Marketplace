from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from catalog.forms import ProductForm
from catalog.models import Product, Category
from catalog.services import get_cached_products, get_cached_categories, clear_products_cache, clear_category_cache, \
    get_category_with_stats, get_products_by_category


class ProductListView(ListView):
    """Класс ProductListView(ListView) - это класс-представление на основе классов (CBV) в
    Django для отображения списка продуктов с низкоуровневым кешированием."""

    model = Product
    template_name = "product_list.html"
    paginate_by = 12
    context_object_name = 'products'

    def get_queryset(self):
        return get_cached_products(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_cached_categories()

        products = self.get_queryset()
        context['total_products_count'] = len(products)

        if self.request.user.is_staff:
            # Для staff показываем детальную статистику
            all_products = Product.objects.all()
            context['published_count'] = all_products.filter(status='published').count()
            context['draft_count'] = all_products.filter(status='draft').count()
            context['total_in_db'] = all_products.count()

        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Класс ProductDetailView(DetailView) - это класс-представление для отображения
    детальной информации об одном объекте."""

    form_class = ProductForm
    model = Product
    template_name = "product_detail.html"

    def get_object(self, queryset=None):
        cache_key = f'product_detail_{self.kwargs.get("pk")}'
        product = cache.get(cache_key)

        if product is None:
            product = super().get_object(queryset)
            cache.set(cache_key, product, 60 * 15)

        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.object
        cache_key = f'product_context_{product.pk}'
        cached_context = cache.get(cache_key)

        if cached_context is None:
            context['related_products'] = Product.objects.filter(
                category=product.category
            ).exclude(pk=product.pk).filter(status='published')[:4]

            cache.set(cache_key, {
                'related_products': context['related_products']
            }, 60 * 15)
        else:
            context.update(cached_context)

        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Класс ProductCreateView(CreateView) - это класс-представление для создания новых
    объектов."""

    model = Product
    template_name = "create_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user

        cache.delete('product_list')
        cache.delete('product_list_staff')

        response = super().form_valid(form)
        return response


class OwnerRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки, что пользователь является владельцем продукта."""

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Класс ProductUpdateView(UpdateView) - это класс-представление для редактирования
    существующих объектов."""

    model = Product
    template_name = "update_product.html"
    form_class = ProductForm

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", args=[self.kwargs.get("pk")])

    def form_valid(self, form):
        response = super().form_valid(form)

        clear_products_cache()
        if self.object.category_id:
            clear_category_cache(self.object.category_id)

        return response


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Класс ProductDeleteView(DeleteView) - это класс-представление для удаления объектов."""

    model = Product
    template_name = "delete_product.html"
    success_url = reverse_lazy("catalog:product_list")

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return obj.owner == user or user.groups.filter(name='moderator').exists()

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        category_id = obj.category_id if obj.category else None

        response = super().delete(request, *args, **kwargs)

        clear_products_cache()
        if category_id:
            clear_category_cache(category_id)

        return response


@login_required
def unpublish_product(request, product_id):
    """Функция unpublish_product — это представление Django, защищенное декоратором
    @login_required, которое позволяет авторизованным пользователям с разрешением
    'catalog.can_unpublish_product' отменить публикацию продукта"""
    if not request.user.has_perm('catalog.can_unpublish_product'):
        return HttpResponseForbidden("У вас нет прав отменять публикацию продукта.")

    product = get_object_or_404(Product, id=product_id)
    product.status = 'draft'
    product.save()

    cache.delete(f'product_detail_{product_id}')
    cache.delete(f'product_context_{product_id}')
    cache.delete('product_list')
    cache.delete('product_list_staff')

    return redirect('catalog:product_list')


@login_required
def delete_product(request, product_id):
    """Функция delete_product — это представление Django, защищенное декоратором
    @login_required, которое позволяет авторизованным пользователям удалять продукты,
    только если они являются владельцами продукта или состоят в группе Модератор продуктов"""
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    if not (product.owner == user or user.groups.filter(name='Модератор продуктов').exists()):
        return HttpResponseForbidden("У вас нет прав удалять продукт.")

    product.delete()

    cache.delete(f'product_detail_{product_id}')
    cache.delete(f'product_context_{product_id}')
    cache.delete('product_list')
    cache.delete('product_list_staff')

    return redirect('catalog:product_list')


class CategoryDetailView(ListView):
    """
    Представление для отображения продуктов в конкретной категории
    """
    model = Product
    template_name = 'category_detail.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        """
        Получаем продукты категории через сервисную функцию
        """
        self.category_id = self.kwargs['pk']
        return get_products_by_category(self.category_id, self.request.user)

    def get_context_data(self, **kwargs):
        """
        Добавляем информацию о категории и статистику в контекст
        """
        context = super().get_context_data(**kwargs)
        category_data = get_category_with_stats(self.category_id, self.request.user)

        if category_data:
            context['category'] = category_data['category']
            context['total_products_count'] = category_data['total_products']
            context['published_products_count'] = category_data['published_products']
            context['draft_products_count'] = category_data['draft_products']

            products = self.get_queryset()
            context['displayed_products_count'] = len(products)

            user = self.request.user
            context['show_admin_info'] = (
                    user.is_staff or
                    user.is_superuser or
                    user.groups.filter(name='Модератор продуктов').exists()
            )
        else:
            context['category'] = None
            context['total_products_count'] = 0
            context['displayed_products_count'] = 0

        return context


def contacts(request):
    """
    Функция contacts — это контроллер (представление) в Django, который обрабатывает
    отображение страницы контактов и приём данных из формы обратной связи.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        return HttpResponse("Сообщение получено, {}!".format(name))

    return render(request, "contacts.html")
