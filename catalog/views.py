from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Product


def product_list(request):
    """
    Функция product_list — это контроллер (представление) в Django, который отвечает за
    отображение списка всех товаров.
    Описание работы функции:
    products = Product.objects.all() — выполняется запрос к базе данных для получения
    всех объектов модели Product.
    context = {"products": products} — формируется словарь контекста, который содержит
    полученный список товаров под ключом "products".
    return render(request, "product_list.html", context) — функция возвращает HTTP-ответ,
    в котором рендерится HTML-шаблон product_list.html с переданным контекстом.
    В шаблоне можно использовать переменную products для отображения списка товаров.
    """
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "product_list.html", context)


def product_detail(request, pk):
    """
    Функция product_detail — это контроллер (представление) в Django, который отвечает
    за отображение подробной информации о конкретном товаре.
    Описание работы функции:
    product = get_object_or_404(Product, pk=pk) — пытается получить объект модели Product
    с первичным ключом (pk), переданным в функцию. Если товар с таким pk не найден,
    возвращается ошибка 404 (страница не найдена).
    context = {"product": product} — формируется словарь контекста, содержащий найденный
    объект товара под ключом "product".
    return render(request, "product_detail.html", context) — функция возвращает HTTP-ответ,
    в котором рендерится HTML-шаблон product_detail.html с переданным контекстом.
    В шаблоне можно использовать переменную product для отображения подробной информации о товаре.
    """
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "product_detail.html", context)


def contacts(request):
    """
    Функция contacts — это контроллер (представление) в Django, который обрабатывает
    отображение страницы контактов и приём данных из формы обратной связи.

    Описание работы функции:
    Проверяется метод запроса:
    Если request.method == "POST", значит пользователь отправил форму с данными.
    Из POST-запроса извлекаются значения полей: name, phone и message с помощью request.
    POST.get().
    Возвращается простой HTTP-ответ с сообщением благодарности, в котором используется
    имя пользователя (name).
    Если запрос не POST (обычно GET), функция рендерит и возвращает шаблон contacts.html,
    который содержит форму для ввода контактных данных.
    Таким образом, функция обрабатывает как отображение формы обратной связи, так и получение
    и подтверждение отправленных пользователем данных.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        return HttpResponse("Сообщение получено, {}!".format(name))
    return render(request, "contacts.html")
