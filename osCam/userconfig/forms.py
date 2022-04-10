from cProfile import label
from ipaddress import ip_address
from pydoc import describe
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import ChoiceField
from .models import Network, RaspberryPi, Camera, Storage, camera_view
from django import forms    
from django.forms import ModelForm

# Class for Network form
# uses the Network model

class NetworkEntryForm( ModelForm ):
    home_ip_address = forms.CharField(label='home ip address',
        widget=forms.TextInput(attrs={'size':'80', 'class':"form-control"})
        )
    camera_ip_address = forms.CharField(label='camera ip address',
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
    
    class Meta:
        model = Camera 
        fields = (
            'device_name', 
            'ip_address',
            'port',
            )

class ViewForm( ModelForm ):
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
        choices=(('h264', 'h264'), ('mjpeg', 'mjpeg'), ('avi', 'avi')),)

    class Meta:
        model = camera_view
        fields = (
            'recording',
            'fps',
            'invert',
            'mirror',
            'codec',)


class StorageForm( ModelForm ):
    record_to_device = forms.BooleanField(required=False, label='record to device',)
    record_to_cloud = forms.BooleanField(required=False, label='record to cloud',)
    file_path = forms.CharField(max_length=255, required=False, label='file path',)
    max_space = forms.IntegerField(required=False, label='max space',)
    time_to_live = forms.IntegerField(required=False, label='time to live',)
    archive = forms.BooleanField(required=False, label='archive',)
    length_of_record = forms.IntegerField(required=False, label='length of record',)
    codec = forms.ChoiceField(
        choices=(('h264', 'h264'), ('mjpeg', 'mjpeg'), ('avi', 'avi')),)
    
    class Meta:
        model = Storage
        fields = (
            'record_to_device',
            'record_to_cloud',
            'file_path',
            'max_space',
            'time_to_live',
            'archive',
            'length_of_record',
            'codec',)