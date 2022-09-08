from decimal import Decimal
from django import forms
from django.core.validators import MinValueValidator
from product.models import Product, Category
from mptt.forms import TreeNodeChoiceField


class ProductAddForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ("name", "category", "image",
                  "price", "stock", "available")

    name = forms.CharField(
        label="",
        help_text="",
        min_length=3,
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Название"}))

    category = TreeNodeChoiceField(
        label="",
        queryset=Category.objects
        .only("name", "pk"),
        initial="",
        required=True,
        help_text="",
        widget=forms.Select(
            attrs={"class":
                   "form-control",
                   "placeholder":
                   "Категория"}))

    price = forms.DecimalField(
        validators=[MinValueValidator(Decimal('1.0'))],
        max_digits=10,
        label="",
        widget=forms.NumberInput(
            attrs={"class": "form-control",
                   "min": "1.0",
                   "placeholder": "Цена ед. товара"}))

    stock = forms.DecimalField(
        validators=[MinValueValidator(Decimal('1.0'))],
        max_digits=10,
        label="",
        widget=forms.NumberInput(
            attrs={"class": "form-control",
                   "min": "1.0",
                   "placeholder": "Кол-во товара (шт)"}))

    available = forms.BooleanField(
        initial=True,
        required=False,
        label="Доступен",
        widget=forms.CheckboxInput(
            attrs={"checked": True}))


class CategoryAddForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ("name", "parent")

    name = forms.CharField(
        label="",
        help_text="",
        min_length=3,
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Название"}))

    parent = TreeNodeChoiceField(
        label="Родительская категория",
        queryset=Category.objects
        .only("name", "pk"),
        initial=0,
        required=False,
        help_text="",
        widget=forms.Select(
            attrs={"class":
                   "form-control",
                   "placeholder":
                   "Родительская категория"}))
