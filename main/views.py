from django.shortcuts import render, redirect, get_object_or_404, reverse   # Add import redirect at this line
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  # Already imported
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.utils.html import strip_tags
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError

@login_required(login_url='/login')
def show_main(request):

    context = {
        'project_name': 'Loom and Harvest',
        'app_name': 'main',
        'developer_name': request.user.username,
        'class_name': 'KKI',
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
    data = Product.objects.filter(user=request.user)  # Fetch all Product objects
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.filter(user=request.user)  # Fetch all Product objects
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

        # Validate password strength
        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password', e)

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            try:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists.")
                    return redirect('main:register')

                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, "User registered successfully.")
                return redirect('main:login')

            except IntegrityError:
                messages.error(request, "An error occurred while creating the user.")
                return redirect('main:register')

        else:
            for field, error in form.errors.items():
                messages.error(request, f'{field}: {error}')

    return render(request, 'register.html')


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

@csrf_exempt
@require_POST
def add_Product_ajax(request):
    name = strip_tags(request.POST.get("name"))
    price = request.POST.get("price")
    description = strip_tags(request.POST.get("description"))
    stock = request.POST.get("stock")
    category = strip_tags(request.POST.get("category", 'Uncategorized'))
    user = request.user

    # Validate inputs
    try:
        if not name.strip() or not description.strip() or not category.strip():
            return JsonResponse({'error': 'Name, description, and category cannot be empty.'}, status=400)

        try:
            price = float(price)
            if price < 0:
                raise ValueError
        except ValueError:
            return JsonResponse({'error': 'Price must be a positive number.'}, status=400)

        try:
            stock = int(stock)
            if stock < 0:
                raise ValueError
        except ValueError:
            return JsonResponse({'error': 'Stock must be a non-negative integer.'}, status=400)

        # Create new Product
        new_product = Product(
            name=name,
            price=price,
            description=description,
            stock=stock,
            category=category,
            user=user
        )

        # Validate model fields
        new_product.full_clean()
        new_product.save()

        return JsonResponse({'message': 'Product created successfully'}, status=201)

    except ValidationError as e:
        error_messages = []
        for field, errors in e.message_dict.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")
        return JsonResponse({'error': ' '.join(error_messages)}, status=400)

    except Exception as e:
        return JsonResponse({'error': 'An error occurred while adding the product.'}, status=400)
