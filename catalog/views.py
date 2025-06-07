from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from catalog.models import Product


class ProductListView(ListView):
    model = Product

class ProductDetailView(DetailView):
    model = Product

class CatalogContactsView(View):
    def get(self, request):
        return render(request, 'catalog/contacts.html')

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get("phone")
        message = request.POST.get('message')
        return HttpResponse(
                    f"Спасибо, {name}! Ваше сообщение получено. Мы свяжемся с вами по вашему контактному номеру - {phone}."
                )
