from django import forms
from userconfig.models import CustomUser


class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'size': '30'}))

    class Meta():
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        )
        help_texts = {'username': None}
