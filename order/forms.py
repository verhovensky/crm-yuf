from django import forms
from order.models import Order
from client.models import Client
from django.core.validators import MinValueValidator, RegexValidator
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.utils import timezone

# Delivery time validation
no_past_date_validator = MinValueValidator(
    limit_value=timezone.localtime(),
    message="Нельзя указать дату в прошлом!")


class OrderCreateForm(forms.ModelForm):

    new_client = forms.BooleanField(
        label="Новый клиент",
        required=False,
        widget=forms.CheckboxInput(
            attrs={"placeholder": "Новый клиент",
                   "class": "new-client"}))

    class Meta:
        model = Order
        fields = ("new_client", "for_other",
                  "this_order_client", "full_name",
                  "address", "phone", "delivery_time",
                  "self_pick", "cash_on_delivery",
                  "description")

    this_order_client = forms.ModelChoiceField(
        label="Выберите клиента:",
        queryset=Client.objects.
            only("name", "pk", "phone_number").
            order_by("name"),
        initial=0,
        required=False,
        help_text="",
        widget=forms.Select(
            attrs={"class": "form-control selected-client",
                   "placeholder": "Выберите заказчика"}))

    address = forms.CharField(
        label="",
        help_text="",
        min_length=8,
        max_length=250,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control new-address",
                   "placeholder": "Адрес доставки"}))

    phone = forms.CharField(
        label="",
        help_text="",
        required=False,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,16}$",
                message="Телефон должен быть в формате: +700112299"
                        " Макс. длинна = 16 знаков")],
        widget=forms.TextInput(
            attrs={"class": "form-control new-phone",
                   "placeholder": "Телефон получателя"}))

    full_name = forms.CharField(
        label="",
        help_text="",
        min_length=3,
        max_length=32,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control new-fullname",
                   "placeholder": "Имя получателя"}))

    delivery_time = forms.DateTimeField(
        label="",
        help_text="",
        validators=[no_past_date_validator],
        required=True,
        input_formats=["%m/%d/%Y %H:%M"],
        widget=DateTimePickerInput(attrs={
            "class": "form-control datetimepicker-input",
            "data-target": "#datetimepicker1",
            "placeholder": "Время доставки",
            "format": "%m/%d/%Y %H:%M"}))

    description = forms.CharField(
        label="",
        help_text="",
        max_length=500,
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control",
                   "placeholder":
                       "Другие примечания / пожелания",
                   "width": "50%", "cols": "60",
                   "rows": "10", }))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["for_other"]:
            self.required_fields(["full_name", "address",
                                  "phone", "this_order_client"])
        if cleaned_data["new_client"]:
            self.required_fields(["full_name", "address", "phone"])
        if not cleaned_data["for_other"] \
                and not cleaned_data["new_client"]:
            self.required_fields(["this_order_client", "address"])
        return self.cleaned_data

    def required_fields(self, fields):
        for field in fields:
            if not self.cleaned_data.get(field, ""):
                msg = forms.ValidationError(
                    "Это поле обязательно!")
                self.add_error(field, msg)


class OrderChangeForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("full_name", "address", "phone",
                  "status", "description")

    full_name = forms.CharField(
        label="",
        help_text="",
        min_length=3,
        max_length=32,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control new-fullname",
                   "placeholder": "Имя получателя"}))

    address = forms.CharField(
        label="",
        help_text="",
        min_length=8,
        max_length=250,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control new-address",
                   "placeholder": "Адрес доставки"}))

    phone = forms.CharField(
        label="",
        help_text="",
        required=False,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,16}$",
                message="Телефон должен быть в формате: +700112299"
                        " Макс. длинна = 16 знаков")],
        widget=forms.TextInput(
            attrs={"class": "form-control new-phone",
                   "placeholder": "Телефон получателя"}))

    status = forms.Select(choices=Order.STATUS)

    description = forms.CharField(
        label="",
        help_text="",
        max_length=500,
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control",
                   "placeholder": "Другие примечания / пожелания",
                   "width": "50%", "cols": "60",
                   "rows": "10", }))

    def clean_status(self):
        data = self.cleaned_data["status"]
        if isinstance(data, int) and data <= 5:
            return data
        else:
            raise forms.ValidationError(
                "Значением статуса может быть "
                "только число в пределах 1-5!")
