from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, product_detail, product_list

app_name = CatalogConfig.name

urlpatterns = [
    path("", product_list, name="product_list"),
    path("catalog/<int:pk>/", product_detail, name="product_detail"),
    path("contacts/", contacts, name="contacts"),
]
