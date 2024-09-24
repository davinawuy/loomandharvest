from django.shortcuts import render, redirect, get_object_or_404   # Add import redirect at this line
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required(login_url='/login')
def show_main(request):
    products= Product.objects.filter(user=request.user)

    context = {
        'project_name': 'Loom and Harvest',
        'app_name': 'main',
        'developer_name': request.user.username,
        'class_name': 'KKI',
        'products': products,
        'last_login': request.COOKIES['last_login'],

    }
    return render(request, 'main.html', context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user  # Assign the current user to the product, if applicable
        product.save()
        return redirect('main:show_main')  # Redirect to the main page or product listing

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

def register_user(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was created for ' + form.cleaned_data['username'])
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                response = HttpResponseRedirect(reverse("main:show_main"))
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('main:login')

