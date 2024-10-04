import random

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView

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

    def get(self, request, *args, **kwargs) -> HttpResponse:
        # Получаем или генерируем seed в сессии
        if "random_seed" not in self.request.session:
            self.request.session["random_seed"] = random.randint(1, 1000000)

        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> list[Product]:
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

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def form_valid(self, form) -> HttpResponse:
        messages.success(self.request, "Продукт успешно добавлен!")
        return super().form_valid(form)


class CatalogView(ListView):
    model = Category
    template_name = "catalog/catalogs.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs) -> dict:
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
