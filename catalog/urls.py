from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView,
    ProductDetailView,
    CatalogContactsView,
    ProductUpdateView,
    ProductCreateView,
    ProductDeleteView,
    CategoryListView,
    ProductsByCategoryView,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("contacts/", CatalogContactsView.as_view(), name="contacts"),
    path("main/", ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/new/", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("category_list/", CategoryListView.as_view(), name="category_list"),
    path('category/<int:category_id>/', ProductsByCategoryView.as_view(), name='products_by_category'),
]
