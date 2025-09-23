from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, product_list

app_name = CatalogConfig.name

urlpatterns = [
    path("", product_list),
    path("contacts/", contacts, name="contacts"),
]
