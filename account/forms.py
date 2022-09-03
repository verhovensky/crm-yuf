from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from bootstrap_datepicker_plus.widgets import DatePickerInput
from account.models import phone_regex
from django import forms

User = get_user_model()


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",
                  "password1", "password2")


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",
                  "date_of_birth", "phone_number", "photo")

    date_of_birth = forms.DateField(
        label="Дата рождения",
        help_text="",
        widget=DatePickerInput(
            attrs={"class": "form-control datepicker-input",
                   "data-target": "#datebirth",
                   "placeholder": "Дата рождения",
                   "format": "%m/%d/%Y"}),
        input_formats=("%m/%d/%Y",),
        required=False)

    first_name = forms.CharField(
        label="",
        help_text="",
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control first_name",
                   "placeholder": "Имя"}))

    last_name = forms.CharField(
        label="",
        help_text="",
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control last_name",
                   "placeholder": "Фамилия"}))

    email = forms.EmailField(
        label="",
        help_text="",
        max_length=150,

        widget=forms.TextInput(
            attrs={"class": "form-control last_name",
                   "readonly": True}))

    phone_number = forms.CharField(
        label="",
        help_text="",
        max_length=16,
        validators=(phone_regex,),
        widget=forms.TextInput(
            attrs={"class": "form-control phone_number",
                   "placeholder": "Мобильный телефон"}))

    photo = forms.FileField(
        label="",
        help_text="",
        widget=forms.FileInput(
            attrs={"class": "form-file"}))
