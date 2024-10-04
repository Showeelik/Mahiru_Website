from django.urls import path

from .views import CatalogView, ProductCreateView, ProductDetailView, HomeView, ContactsView

urlpatterns = [
    path("products", HomeView.as_view(), name="home"),
    path("catalogs", CatalogView.as_view(), name="catalogs"),
    path("product/add", ProductCreateView.as_view(), name="catalog_add"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product"),
    path("contacts", ContactsView.as_view(), name="contacts"),
]
