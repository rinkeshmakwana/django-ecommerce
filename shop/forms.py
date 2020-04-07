from django import forms
from .models import Product


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_description', 'product_price', 'product_rating']


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_image']
