from django.shortcuts import render, redirect, get_object_or_404, reverse   # Add import redirect at this line
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  # Already imported
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
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
        # Add success message after product creation
        messages.success(request, f'Product "{product.name}" was created successfully!')
        return redirect('main:show_main')  # Redirect to the main page or product listing

    context = {'form': form}
    return render(request, "create_product.html", context)

def edit_Product(request, id):
    # Get product entry based on id, raise 404 if not found
    product = get_object_or_404(Product, pk=id)

    # Set product entry as an instance of the form
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        # Save form and return to the main page
        form.save()
        # Add success message after product edit
        messages.success(request, f'Product "{product.name}" was edited successfully!')
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form, 'product': product}
    return render(request, "edit_Product.html", context)

def delete_Product(request, id):
    product = Product.objects.get(pk=id)
    product_name = product.name
    product.delete()
    # Set the delete message as an error (which we will style as red)
    messages.error(request, f'Product "{product_name}" was deleted successfully!')
    return HttpResponseRedirect(reverse('main:show_main'))

def show_xml(request):
    data = Product.objects.all()  # Fetch all Product objects
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()  # Fetch all Product objects
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


def register_user(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Create a new user using the cleaned data
            user = User.objects.create_user(username=username, password=password)
            user.save()
            
            messages.success(request, f'Account was created for {username}')
            return redirect('main:login')  # Ensure 'main:login' exists in your urls.py
        
        else:
            # If form is not valid, capture the errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
                    
    context = {'form': form}
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
            # If form is invalid, send an error message
            messages.error(request, 'Invalid username or password.')
            return redirect('main:login')  # Redirect back to the login page

    form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('main:login')
