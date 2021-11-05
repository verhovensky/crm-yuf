from .models import UserProfile, User
from bootstrap_datepicker_plus import DatePickerInput
from django import forms


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):

    date_of_birth = forms.DateTimeField(label="Дата рождения",
                              help_text="",
                              widget=DatePickerInput
                              (attrs={'class': 'form-control datepicker-input',
                                      'data-target': '#datepicker1',
                                      'placeholder': 'Дата рождения',
                                      'format': '%m/%d/%Y'}))

    class Meta:
        model = UserProfile
        fields = ('date_of_birth', 'phone_number', 'photo')
