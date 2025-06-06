from django.urls import path

from catalog import views
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.index, name="base"),
    path("contacts/", views.contacts, name="contacts"),
    path('products_list/', views.products_list, name='products_list'),
    path("product_detail/<int:product_id>/", views.product_detail, name="product_detail")
]
