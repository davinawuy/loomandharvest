from django.shortcuts import render, redirect, get_object_or_404   # Add import redirect at this line
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse
from django.core import serializers


def show_main(request):
    products= Product.objects.all()

    context = {
        'project_name': 'Loom and Harvest',
        'app_name': 'main',
        'developer_name': 'Alano Davin Mandagi Awuy',
        'class_name': 'KKI',
        'products': products
    }
    return render(request, 'main.html', context)

def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new product to the database
            return redirect('main:show_main')  # Redirect to the product listing page
    else:
        form = ProductForm()  # Display an empty form for GET requests

    context = {'form': form}
    return render(request, "create_product.html", context)


def show_xml(request):
    data = Product.objects.all()  # Fetch all Product objects
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# View to return data in JSON format
def show_json(request):
    data = Product.objects.all()  # Fetch all Product objects
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")