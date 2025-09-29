from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from catalog.models import Product


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"


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
