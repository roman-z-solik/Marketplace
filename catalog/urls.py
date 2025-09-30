from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
    contacts,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("catalog/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("contacts/", contacts, name="contacts"),
    path("catalog/create_product/", ProductCreateView.as_view(), name="create_product"),
    path(
        "catalog/update_product/<int:pk>/",
        ProductUpdateView.as_view(),
        name="update_product",
    ),
    path(
        "catalog/delete_product/<int:pk>/",
        ProductDeleteView.as_view(),
        name="delete_product",
    ),
]
