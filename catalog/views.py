from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Product


def product_list(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, "base.html", context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        return HttpResponse("Сообщение получено, {}!".format(name))
    return render(request, "contacts.html")
