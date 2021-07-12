from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Profile


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'phone', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('name', 'lastName','mobile_no','alter_mobile_no','address')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'textinputclass'}),
            'lastName': forms.TextInput(attrs={'class': 'textinputclass'}),
        }