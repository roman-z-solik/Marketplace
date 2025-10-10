from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
    contacts, CategoryDetailView,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("contacts/", contacts, name="contacts"),
    path("catalog/create/", ProductCreateView.as_view(), name="create_product"),
    path("catalog/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("catalog/<int:pk>/update/", ProductUpdateView.as_view(), name="update_product"),
    path("catalog/<int:pk>/delete/", ProductDeleteView.as_view(), name="delete_product"),
path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
]
