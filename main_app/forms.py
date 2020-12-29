from django import forms
from django.contrib.auth import get_user_model

from phonenumber_field.formfields import PhoneNumberField


class RegistrationForm(forms.Form):

    email = forms.EmailField()
    fio = forms.CharField(max_length=255)
    adress = forms.CharField(widget=forms.TextInput)
    phone = PhoneNumberField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(username=email).exists():
            raise forms.ValidationError('Пользовтель с таким email существует')
        return email
