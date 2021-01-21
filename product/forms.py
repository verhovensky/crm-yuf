from django import forms

from .models import Product

class ProductAddForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'category', 'image', 'price', 'stock', 'available')