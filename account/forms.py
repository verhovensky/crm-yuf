from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from bootstrap_datepicker_plus import DatePickerInput
from django import forms


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email',
                  'password1', 'password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'phone_number', 'photo']

    date_of_birth = forms.DateField(label="Дата рождения",
                                    help_text="",
                                    widget=DatePickerInput
                                    (attrs={'class': 'form-control datepicker-input',
                                            'data-target': '#datebirth',
                                            'placeholder': 'Дата рождения',
                                            'format': '%m/%d/%Y'}),
                                    input_formats=['%m/%d/%Y'],
                                    required=False)
