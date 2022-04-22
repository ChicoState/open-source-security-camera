from django.db.models.fields import NullBooleanField
from core.models import *
from django import forms
from django.core import validators
from django.contrib.auth.models import User

from crispy_forms.layout import Field, Layout, Div, HTML, ButtonHolder, Submit
from crispy_forms.helper import FormHelper


class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        help_texts = {
            'username': None
        }



