from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Product, ProductImages


class AddUser(forms.ModelForm):
    product_name = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), label= 'Product Name*')
    class Meta():
        model = Product
        fields = [
            'product_name'
        ]

class ProductAdd(forms.ModelForm):
    image = forms.FileField(label= 'Display Image*')
    price = forms.CharField(label= 'Price (in dollar)')
    class Meta:
        model = Product
        exclude = ('user',)
        fields = [
            'category',
            'product_name',
            'brand',
            'condition',
            'price',
            'description',
            'number',
            'city',
            'country',
            'image'
        ]
        

class ImageAdd(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label= 'Detail Images*')
    class Meta:
        model = ProductImages
        exclude = ('product',)
        fields = [
            'images',
        ]
