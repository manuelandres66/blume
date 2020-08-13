from django import forms
from django.contrib.auth.models import User

class Entrar(forms.Form):
    usuario = forms.CharField(max_length=1000)
    password = forms.CharField(max_length=1000, widget=forms.PasswordInput)