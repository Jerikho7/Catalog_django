from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

from catalog.forms import ProductForm, ModeratorProductForm
from catalog.models import Product, Category
from catalog.services import get_products_by_category


class CategoryListView(ListView):
    model = Category
    template_name = "catalog/category_list.html"
    context_object_name = "categories"

class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        queryset = cache.get("products_queryset")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("products_queryset", queryset, 60 * 15)
        return queryset

class ProductsByCategoryView(ListView):
    model = Product
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        context['category'] = get_object_or_404(Category, id=category_id)
        return context

@method_decorator(cache_page(60 * 5), name="dispatch")
class ProductDetailView(DetailView):
    model = Product


class CatalogContactsView(View):
    def get(self, request):
        return render(request, "catalog/contacts.html")

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(
            f"Спасибо, {name}! Ваше сообщение получено. Мы свяжемся с вами по вашему контактному номеру - {phone}."
        )


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_create.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_create.html"
    success_url = reverse_lazy("catalog:product_list")

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("product.can_unpublish_product") and user.has_perm("product.delete_product"):
            return ModeratorProductForm
        raise PermissionDenied

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "catalog/product_delete.html"
    success_url = reverse_lazy("catalog:product_list")

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return product.owner == user or user.has_perm('catalog.delete_product')

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет прав на удаление этого продукта.")
