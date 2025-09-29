from django.http import HttpResponse
from django.shortcuts import render
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
    model = Product
    template_name = "product_list.html"


class ProductDetailView(DetailView):
    form_class = ProductForm
    model = Product
    template_name = "product_detail.html"


class ProductCreateView(CreateView):
    model = Product
    template_name = "create_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "update_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", args=[self.kwargs.get("pk")])


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "delete_product.html"
    success_url = reverse_lazy("catalog:product_list")


def contacts(request):
    """
    Функция contacts — это контроллер (представление) в Django, который обрабатывает
    отображение страницы контактов и приём данных из формы обратной связи.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        return HttpResponse("Сообщение получено, {}!".format(name))
    return render(request, "contacts.html")
