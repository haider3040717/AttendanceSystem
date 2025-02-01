from django import forms
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2',]

    def __init__(self, *args, **kwargs):
        super(AccountCreationForm, self).__init__(*args, **kwargs)




class AccountAuthenticationForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']




class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number_1', 'phone_number_2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number 1'}),
            'phone_number_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number 2'}),
        }