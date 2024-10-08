from django.forms import ModelForm
from main.models import Product
from django.utils.html import strip_tags

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



#Create a form to add a product and clean the data
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "stock", "category"]
    def clean_name(self):
        name = self.cleaned_data['name']
        return strip_tags(name)
    def clean_description(self):
        description = self.cleaned_data['description']
        return strip_tags(description)
    def clean_category(self):
        category = self.cleaned_data['category']
        return strip_tags(category)
    
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