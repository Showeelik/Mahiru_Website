from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),
    path("catalog/add/", views.add_product, name="catalog_add"),
    path("contacts/", views.contacts, name="contacts"),
]
