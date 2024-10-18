import random

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ProductForm
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
    paginate_by = 4  # Показывать 4 продуктов на странице

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Возвращает URL для редиректа.

        Args:
            request (HttpRequest): _request_

        Returns:
            HttpResponse:
        """
        # Получаем или генерируем seed в сессии
        if "random_seed" not in self.request.session:
            self.request.session["random_seed"] = random.randint(1, 1000000)

        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> list[Product]:
        """
        Возвращает список продуктов.

        Returns:
            list[Product]:
        """
        # Используем seed для случайной сортировки продуктов
        random_seed = self.request.session["random_seed"]

        products = list(Product.objects.filter(is_published=True))
        random.Random(random_seed).shuffle(products)
        return products


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalogs")

    def get_context_data(self, **kwargs) -> dict:
        """Возвращает контекст для шаблона.

        Returns:
            dict:
        """
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def form_valid(self, form) -> HttpResponse:
        """
        Обрабатывает валидацию формы.

        Args:
            form (ProductForm): _form_

        Returns:
            HttpResponse:
        """
        messages.success(self.request, "Продукт успешно добавлен!")
        return super().form_valid(form)


class CatalogView(ListView):
    model = Category
    template_name = "catalog/catalogs.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs) -> dict:
        """
        Возвращает контекст для шаблона.


        Args:
            **kwargs: _kwargs_


        Returns:
            dict: контекст для шаблона
        """
        context = super().get_context_data(**kwargs)

        category_id = self.request.GET.get("category")
        selected_category = None

        if category_id:
            selected_category = get_object_or_404(Category, id=category_id)
            selected_category_products = selected_category.products.filter(is_published=True)
            context["selected_category_products"] = selected_category_products
            context["selected_category"] = selected_category
        else:
            categories = Category.objects.all()
            for category in categories:
                category.published_products = category.products.filter(is_published=True)
            context["categories"] = categories

        return context


class ContactsView(ListView):
    model = Category
    template_name = "catalog/contacts.html"


class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = "product"
    success_url = reverse_lazy("catalogs")

    def delete(self, request, *args, **kwargs) -> HttpResponse:
        """
        Удаляет продукт.

        Args:
            request (HttpRequest): _request_
            *args: _args_
            **kwargs: _kwargs_


        Returns:
            HttpResponse:
        """
        messages.success(self.request, "Продукт успешно удалён!")
        return super().delete(request, *args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self) -> str:
        """
        Возвращает URL для редиректа.

        Returns:
            str:
        """
        return reverse_lazy("product", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs) -> dict:
        """
        Возвращает контекст для шаблона.

        Returns:
            dict:
        """
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def form_valid(self, form) -> HttpResponse:
        """
        Обрабатывает валидацию формы.

        Args:
            form (ProductForm): _form_
        Returns:
            HttpResponse:
        """
        messages.success(self.request, "Продукт успeшно обновлён!")
        return super().form_valid(form)
