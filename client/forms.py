from django import forms

from .models import Client


class ClientAddForm(forms.ModelForm):
    class Meta:
        model = Client
        name = forms.CharField()
        type = forms.ChoiceField()
        phone_number = forms.IntegerField()
        origin = forms.ChoiceField()
        email = forms.EmailField()
        exclude = ('created_by', 'slug',)
