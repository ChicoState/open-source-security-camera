from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import ChoiceField
from .models import Network, RaspberryPi, Camera
from django import forms    
from django.forms import ModelForm

        
class NetworkEntryForm( ModelForm ):
    home_ip_address = forms.CharField(label='description',
        widget=forms.TextInput(attrs={'size':'80', 'class':"form-control"})
        )
    camera_ip_address = forms.CharField(label='description',
        widget=forms.TextInput(attrs={'size':'80', 'class':"form-control"})
        )
    class Meta:
        model = Network 
        fields = ('home_ip_address', 'camera_ip_address')


class CameraEntryForm( ModelForm ):
    model_info = forms.CharField(label='description',
        widget=forms.TextInput(attrs={'size':'80', 'class':"form-control"})
        )
    class Meta:
        model = Camera 
        fields = ('model_info',)

# alternate carera form whoops
# class CameraForm(forms.ModelForm):
#     class Meta():
#         model = Camera
#         fields = ('recording', 'fps', 'invert', 'mirror', 'codec', 'camera_index', 'device_name', 'ip_address', 'port', 'username', 'password')


# class RaspberryPiEntryForm( ModelForm ):
#     model_num = forms.CharField(label='model number',
#         widget=forms.TextInput(attrs={'size':'80', 'class':"form-control"})
#         )
#     model_name = models.CharField(label='model name',
#         widget=forms.TextInput(attrs={'size':'80', 'class':"form-control"})
#         )
#     class Meta:
#         model = RaspberryPi 
#         fields = ('model_num', 'model_name')
