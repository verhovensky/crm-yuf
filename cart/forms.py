from django import forms
from decimal import Decimal
from django.core.validators import MinValueValidator


class CartAddProductForm(forms.Form):

    # TODO: not 0 quantity, not - quantity

    quantity = forms.DecimalField(
        validators=[MinValueValidator(Decimal('1.0'))],
        max_digits=10,
        label="",
        widget=forms.NumberInput(
            attrs={"class": "text-center form-control",
                   "style": "max-width: 19em;",
                   "min": "1.0",
                   "placeholder": "Добавить в заказ"}))
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput)
