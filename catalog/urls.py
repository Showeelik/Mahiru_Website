from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),
    path("catalog/add/", views.add_product, name="catalog_add"),
    path("catalog/<int:pk>/", views.product_detal, name="product"),
    path("contacts/", views.contacts, name="contacts"),
]
