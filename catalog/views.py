from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from catalog.models import Product


def product_list(request):
    """
    Функция product_list — это контроллер (представление) в Django, который отвечает за
    отображение списка всех товаров.
    """
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "product_list.html", context)


def product_detail(request, pk):
    """
    Функция product_detail — это контроллер (представление) в Django, который отвечает
    за отображение подробной информации о конкретном товаре.
    """
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "product_detail.html", context)


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
