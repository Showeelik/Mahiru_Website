from django.urls import path

from .views import (CatalogView, ContactsView, HomeView, ProductCreateView, ProductDeleteView, ProductDetailView,
                    ProductUpdateView)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("catalogs", CatalogView.as_view(), name="catalogs"),
    path("product/add", ProductCreateView.as_view(), name="catalog_add"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product"),
    path("product/<int:pk>/delete", ProductDeleteView.as_view(), name="product_delete"),
    path("product/<int:pk>/edit", ProductUpdateView.as_view(), name="product_update"),
    path("contacts", ContactsView.as_view(), name="contacts"),
]
