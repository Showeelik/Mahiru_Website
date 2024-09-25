import random

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Product


# Create your views here.
def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        category_id = request.POST.get("category")
        image = request.FILES.get("image")

        # Создаем новый продукт
        product = Product(name=name, description=description, price=price, category_id=category_id, image=image)
        product.save()

        messages.success(request, "Продукт успешно добавлен!")
        return redirect("catalog")  # Перенаправление на страницу каталога

    # Получаем все категории для выбора
    categories = Category.objects.all()
    return render(request, "catalog/catalog_add.html", {"categories": categories})


def home(request):
    # Получаем seed из сессии или генерируем новый
    if "random_seed" not in request.session:
        request.session["random_seed"] = random.randint(1, 1000000)

    random_seed = request.session["random_seed"]

    # Используем seed для сортировки продуктов
    products = list(Product.objects.all())
    random.Random(random_seed).shuffle(products)

    paginator = Paginator(products, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "catalog/home.html", context)


def catalog(request):
    categories = Category.objects.all()

    category_id = request.GET.get("category")
    selected_category = None

    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)

    context = {"categories": categories, "selected_category": selected_category, "request": request}

    return render(request, "catalog/catalogs.html", context)


def contacts(request):
    if request.method == "POST":
        # Получение данных из формы
        name = request.POST.get("name")
        message = request.POST.get("message")
        # Обработка данных (например, сохранение в БД, отправка email и т. д.)
        # Здесь мы просто возвращаем простой ответ
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, "catalog/contacts.html")
