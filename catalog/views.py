from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Product


# Create your views here.
def index(request):
    return render(request, "catalog/base.html")


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(
            f"Спасибо, {name}! Ваше сообщение получено. Мы свяжемся с вами по вашему контактному номеру - {phone}."
        )
    return render(request, "catalog/contacts.html")

def products_list(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'catalog/products_list.html', context=context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "catalog/product_detail.html", context=context)
