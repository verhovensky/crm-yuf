from django import forms
from decimal import Decimal
from django.core.validators import MinValueValidator


class CartAddProductForm(forms.Form):
    quantity = forms.DecimalField(validators=[MinValueValidator(Decimal('1.0'))],
                                  max_digits=10,
                                  label='Количество')
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
