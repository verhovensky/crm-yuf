from django import forms
from .models import Order
from django.core.exceptions import ValidationError
from typing import Union, Any
import pytz
import datetime
from django.utils.timezone import make_aware


def blank_strings(v: Union[str, Any]) -> Union[str, Any, None]:
    if isinstance(v, str) and v.strip() == "":
        return None
    return v


class OrderCreateFormForNewCustomer(forms.ModelForm):
    full_name = forms.CharField(label="",
                                help_text="",
                                widget=forms.TextInput
                                (attrs={'class': 'form-control',
                                        'placeholder': 'ФИО заказчика'}))
    phone = forms.CharField(label="",
                            help_text="",
                            widget=forms.NumberInput
                            (attrs={'class': 'form-control',
                                    'placeholder': 'Моб. телефон'}))
    address = forms.CharField(label="",
                              help_text="",
                              widget=forms.TextInput
                              (attrs={'class': 'form-control',
                                      'placeholder': 'Адрес доставки'}))
    delivery_time = forms.DateTimeField(label="",
                                    help_text="",
                                    widget=forms.DateTimeInput
                                    (attrs={'class': 'form-control',
                                            'placeholder': 'Дата / время доставки'}))
    description = forms.CharField(label="",
                                  help_text="",
                                  widget=forms.Textarea
                                  (attrs={'class': 'form-control',
                                          'placeholder': 'Другие примечания / пожелания'}))

    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'address', 'delivery_time',
                  'self_pick', 'cash_on_delivery', 'description']

    def clean(self):
        cleaned_data = super(OrderCreateFormForNewCustomer, self).clean()

        full_name = blank_strings(cleaned_data.get('full_name'))
        phone = cleaned_data.get('phone')
        address = cleaned_data.get('address')
        delivery_time = cleaned_data.get('delivery_time')
        self_pick = cleaned_data.get('self_pick')
        cash_on_delivery = cleaned_data.get('cash_on_delivery')
        description = cleaned_data.get('description')

        # Values may be None if the fields did not pass previous validations.
        if full_name is not None and phone is not None and address is not None and delivery_time is not None and self_pick is not None and cash_on_delivery is not None and description is not None:
            if (type(delivery_time)) is datetime:
                delivery_time = make_aware(delivery_time, timezone=pytz.timezone("Asia/Bishkek"))
                print(delivery_time)
        else:
            self.add_error(None, ValidationError('Убедитесь что все поля заполнены верно'))
        return cleaned_data
