import random

from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .forms import ProductForm
from .models import Category, Product
from .services import ProductService


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs) -> dict:
        context =  super().get_context_data(**kwargs)
        product_id = self.kwargs["pk"]
        product = ProductService.get_product_by_id(product_id)
        context["product"] = product
        return context



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
        seed = self.request.session["random_seed"]
        products = cache.get(f"products_{seed}")

        if products is None:
            products = ProductService.get_published_products()
            cache.set(f"products_{seed}", products, 60 * 15)

        return products


class ProductCreateView(LoginRequiredMixin, CreateView):
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
        form.instance.owner = self.request.user
        messages.success(self.request, "Продукт успешно добавлен!")
        return super().form_valid(form)


class CatalogView(ListView):
    model = Category
    template_name = "catalog/catalogs.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.get_queryset()        
        return context

    def get_queryset(self) -> list[Category]:
        """
        Возвращает список категорий.

        Returns:
            list[Category]:
        """
        catalogs = cache.get("catalogs")

        if catalogs is None:
            catalogs = Category.objects.all()
            cache.set("catalogs", catalogs, 60 * 15)  # Кэшируем на 15 минут

        return catalogs




class CatalogProductsView(ListView):
    template_name = "catalog/catalog_products.html"
    context_object_name = "products"

    def get_queryset(self) -> list[Product]:
        """
        Возвращает список продуктов в указанной категории.
        """
        category_id = self.kwargs.get("category_id")
        self.category = get_object_or_404(Category, pk=category_id)
        return ProductService.get_published_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        """
        Добавляет информацию о категории в контекст.
        """
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["products"] = self.get_queryset()
        return context


class ContactsView(ListView):
    model = Category
    template_name = "catalog/contacts.html"


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    context_object_name = "product"
    success_url = reverse_lazy("catalogs")
    permission_required = "catalog.can_delete_product"

    def has_permission(self) -> bool:
        product = get_object_or_404(Product, pk=self.kwargs["pk"])
        return super().has_permission() or self.request.user == product.owner

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


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "catalog.can_unpublish_product"

    def has_permission(self) -> bool:
        product = get_object_or_404(Product, pk=self.kwargs["pk"])
        return super().has_permission() or self.request.user == product.owner

    def post(self, request, pk) -> HttpResponse:
        product = get_object_or_404(Product, pk=pk)
        if product.is_published:
            product.is_published = False
            product.save()
            messages.success(request, "Продукт снят с публикации.")
        else:
            messages.warning(request, "Продукт уже снят с публикации.")
        return redirect("product", pk=pk)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
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
