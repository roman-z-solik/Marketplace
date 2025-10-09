from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
from catalog.models import Product


class ProductListView(ListView):
    """Класс ProductListView(ListView) - это класс-представление на основе классов (CBV) в
    Django для отображения списка продуктов."""

    model = Product
    template_name = "product_list.html"

    def get_queryset(self):
        queryset = Product.objects.all()

        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')
        return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Класс ProductDetailView(DetailView) - это класс-представление для отображения
    детальной информации об одном объекте."""

    form_class = ProductForm
    model = Product
    template_name = "product_detail.html"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Класс ProductCreateView(CreateView) - это класс-представление для создания новых
    объектов."""

    model = Product
    template_name = "create_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки, что пользователь является владельцем продукта."""
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class ProductUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    """Класс ProductUpdateView(UpdateView) - это класс-представление для редактирования
    существующих объектов. Только владелец может редактировать."""

    model = Product
    template_name = "update_product.html"
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", args=[self.kwargs.get("pk")])


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Класс ProductDeleteView(DeleteView) - это класс-представление для удаления объектов.
    Удалять может владелец или пользователь с правами модератора (группа 'moderator')."""

    model = Product
    template_name = "delete_product.html"
    success_url = reverse_lazy("catalog:product_list")

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        # Владелец или модератор
        if obj.owner == user:
            return True
        if user.groups.filter(name='moderator').exists():
            return True
        return False


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
    return redirect('product_list')


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
    return redirect('product_list')


def contacts(request):
    """
    Функция contacts — это контроллер (представление) в Django, который обрабатывает
    отображение страницы контактов и приём данных из формы обратной связи.
    """
    if request.method == "POST":
        name = request.POST.get("name")

        return HttpResponse("Сообщение получено, {}!".format(name))
    return render(request, "contacts.html")
