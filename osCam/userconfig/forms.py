from cProfile import label
from ipaddress import ip_address
from pydoc import describe
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
    device_name = forms.CharField(max_length=255, required=True, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Backyard Cam', 
            'class':"form-control"}))
    ip_address = forms.CharField(max_length=255, 
        widget=forms.TextInput(attrs={'placeholder': '10.0.0.94', 'class':"form-control"}))
    port = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': '80', 'class':"form-control"}))
    recording = forms.BooleanField(
        label='enable recording',
        widget=forms.CheckboxInput(),
        required=False)
    fps = forms.ChoiceField(
        choices=((15, '15'), (30, '30'), (60, '60')),)
    invert = forms.BooleanField(
        required=False,
        label='invert image',
        widget=forms.CheckboxInput())
    mirror = forms.BooleanField(
        required=False,
        label='mirror image',
        widget=forms.CheckboxInput())
    codec = forms.ChoiceField(
        choices=(('h264', 'h264'), ('mjpeg', 'mjpeg'),),)
    

    class Meta:
        model = Camera 
        fields = (
            'device_name', 
            'ip_address',
            'port',
            'recording',
            'fps',
            'invert',
            'mirror',
            'codec',)
    

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
