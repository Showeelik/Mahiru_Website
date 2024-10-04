import random

from django.urls import reverse
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Product


# Create your views here.
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    


class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 4  # Показывать 8 продуктов на странице

    def get(self, request, *args, **kwargs):
        # Получаем или генерируем seed в сессии
        if "random_seed" not in self.request.session:
            self.request.session["random_seed"] = random.randint(1, 1000000)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # Используем seed для случайной сортировки продуктов
        random_seed = self.request.session["random_seed"]
        products = list(Product.objects.all())
        random.Random(random_seed).shuffle(products)
        return products

class ProductCreateView(CreateView):
    model = Product
    template_name = "catalog/product_add.html"
    fields = ["name", "description", "price", "category", "image"]
    success_url = "/catalogs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Продукт успешно добавлен!")
        return super().form_valid(form)

class CatalogView(ListView):
    model = Category
    template_name = "catalog/catalogs.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Получаем выбранную категорию через GET параметр
        category_id = self.request.GET.get("category")
        selected_category = None
        
        if category_id:
            selected_category = get_object_or_404(Category, id=category_id)
        
        context["selected_category"] = selected_category
        return context
    
class ContactsView(ListView):
    model = Category
    template_name = "catalog/contacts.html"

# def add_product(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         description = request.POST.get("description")
#         price = request.POST.get("price")
#         category_id = request.POST.get("category")
#         image = request.FILES.get("image")

#         # Создаем новый продукт
#         product = Product(name=name, description=description, price=price, category_id=category_id, image=image)
#         product.save()

#         messages.success(request, "Продукт успешно добавлен!")
#         return redirect("catalog")  # Перенаправление на страницу каталога

#     # Получаем все категории для выбора
#     categories = Category.objects.all()
#     return render(request, "catalog/catalog_add.html", {"categories": categories})


# def home(request):
#     # Получаем seed из сессии или генерируем новый
#     if "random_seed" not in request.session:
#         request.session["random_seed"] = random.randint(1, 1000000)

#     random_seed = request.session["random_seed"]

#     # Используем seed для сортировки продуктов
#     products = list(Product.objects.all())
#     random.Random(random_seed).shuffle(products)

#     paginator = Paginator(products, 8)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     context = {
#         "page_obj": page_obj,
#     }
#     return render(request, "catalog/home.html", context)


# def catalog(request):
#     categories = Category.objects.all()

#     category_id = request.GET.get("category")
#     selected_category = None

#     if category_id:
#         selected_category = get_object_or_404(Category, id=category_id)

#     context = {"categories": categories, "selected_category": selected_category, "request": request}

#     return render(request, "catalog/catalogs.html", context)


# def contacts(request):
#     if request.method == "POST":
#         # Получение данных из формы
#         name = request.POST.get("name")
#         message = request.POST.get("message")
#         # Обработка данных (например, сохранение в БД, отправка email и т. д.)
#         # Здесь мы просто возвращаем простой ответ
#         return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
#     return render(request, "catalog/contacts.html")
