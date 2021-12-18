from django import forms
from .models import Order
from client.models import Client
from django.core.validators import RegexValidator
from bootstrap_datepicker_plus import DateTimePickerInput


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,16}$',
                             message="Введите номер телефона, макс. длинна = 16 знаков")


class OrderCreateFormForNewCustomer(forms.ModelForm):
    full_name = forms.CharField(label="",
                                help_text="",
                                min_length=3,
                                max_length=22,
                                widget=forms.TextInput
                                (attrs={'class': 'form-control',
                                        'placeholder': 'ФИО заказчика'}))
    phone = forms.CharField(label="",
                            help_text="",
                            validators=[phone_regex],
                            widget=forms.NumberInput
                            (attrs={'class': 'form-control',
                                    'placeholder': 'Моб. телефон'}))
    address = forms.CharField(label="",
                              help_text="",
                              min_length=3,
                              max_length=250,
                              widget=forms.TextInput
                              (attrs={'class': 'form-control',
                                      'placeholder': 'Адрес доставки'}))
    delivery_time = forms.DateTimeField(label="",
                              help_text="",
                              widget=DateTimePickerInput
                              (attrs={'class': 'form-control datetimepicker-input',
                                      'data-target': '#datetimepicker1',
                                      'placeholder': 'Время доставки',
                                      'format': '%m/%d/%Y'}))

    description = forms.CharField(label="",
                                  help_text="",
                                  max_length=500,
                                  required=False,
                                  widget=forms.Textarea
                                  (attrs={'class': 'form-control',
                                          'placeholder': 'Другие примечания / пожелания',
                                          'width': "50%", 'cols': "60", 'rows': "10", }))

    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'address', 'delivery_time',
                  'self_pick', 'cash_on_delivery', 'description']


class OrderCreateFormForExistingCustomer(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['this_order_client', 'address', 'delivery_time',
                  'self_pick', 'cash_on_delivery', 'description']

    this_order_client = forms.ModelChoiceField(label="Заказ клиента:",
                                               queryset=Client.objects.all().order_by('name'),
                                               initial=0,
                                               required=True,
                                               help_text="",
                                               widget=forms.Select
                                               (attrs={'class': 'form-control text-input',
                                                       'placeholder': 'Выберите заказчика'}))

    address = forms.CharField(label="",
                              help_text="",
                              min_length=8,
                              max_length=250,
                              required=True,
                              widget=forms.TextInput
                              (attrs={'class': 'form-control',
                                      'placeholder': 'Адрес доставки'}))

    name = forms.CharField(label="",
                              help_text="",
                              min_length=8,
                              max_length=250,
                              required=False,
                              widget=forms.HiddenInput())

    delivery_time = forms.DateTimeField(label="",
                              help_text="",
                              required=True,
                              widget=DateTimePickerInput
                              (attrs={'class': 'form-control datetimepicker-input',
                                      'data-target': '#datetimepicker1',
                                      'placeholder': 'Время доставки',
                                      'format': '%m/%d/%Y'}))

    description = forms.CharField(label="",
                                  help_text="",
                                  max_length=500,
                                  required=False,
                                  widget=forms.Textarea
                                  (attrs={'class': 'form-control',
                                          'placeholder': 'Другие примечания / пожелания',
                                          'width': "50%", 'cols': "60", 'rows': "10", }))
