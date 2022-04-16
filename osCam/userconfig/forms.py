from pydoc import describe
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import ChoiceField
from .models import Network, RaspberryPi, Camera, Storage, CameraView
from django import forms    
from django.forms import ModelForm

# Class for Network Settings
class NetworkEntryForm( ModelForm ):
    homeIpAddress = forms.CharField(label='home ip address', required=False,
        widget=forms.TextInput(attrs={'size':'80', 'class':"form-control"})
        )
    cameraIpAddress = forms.CharField(label='camera ip address', required=False,
        widget=forms.TextInput(attrs={'size':'80', 'class':"form-control"})
        )
    homeNetmask = forms.CharField(label='home netmask', required=False,)

    class Meta:
        model = Network 
        fields = ('homeIpAddress', 'cameraIpAddress', 'homeNetmask',)

# Class for Camera Settings
class CameraEntryForm( ModelForm ):
    deviceName = forms.CharField(max_length=255, required=True, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Backyard Cam', 
            'class':"form-control"}))
    ipAddress = forms.CharField(max_length=255, 
        widget=forms.TextInput(attrs={'placeholder': '10.0.0.94', 'class':"form-control"}))
    port = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': '80', 'class':"form-control"}))

    class Meta:
        model = Camera 
        fields = (
            'deviceName', 
            'ipAddress',
            'port',
            )

# Class for view settings
# this affects how the 'feed' from the camera is 'viewed'
class CameraViewForm( ModelForm ):
    showMotionBoxes = forms.BooleanField(required=False)
    showContours = forms.BooleanField(required=False)
    showText = forms.BooleanField(required=False)
    text = forms.CharField(max_length=255, required=False)
    contrast = forms.IntegerField(required=False)
    brightness = forms.IntegerField(required=False)

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
        model = CameraView
        fields = (
            'showMotionBoxes',
            'showContours',
            'showText',
            'text',
            'contrast',
            'brightness',
            'recording',
            'fps',
            'invert',
            'mirror',
            'codec',)

# class for Storage settings
class StorageForm( ModelForm ):
    recordToDevice = forms.BooleanField(required=False, label='record to device',)
    recordToCloud = forms.BooleanField(required=False, label='record to cloud',)
    filePath = forms.CharField(max_length=255, required=False, label='file path',)
    maxSpace = forms.IntegerField(required=False, label='max space',)
    timeToLive = forms.IntegerField(required=False, label='time to live',)
    archive = forms.BooleanField(required=False, label='archive',)
    lengthOfRecordings = forms.IntegerField(required=False, label='length of record',)
    codec = forms.ChoiceField(
        choices=(('h264', 'h264'), ('mjpeg', 'mjpeg'), ('avi', 'avi')),)
    
    class Meta:
        model = Storage
        fields = (
            'recordToDevice',
            'recordToCloud',
            'filePath',
            'maxSpace',
            'timeToLive',
            'archive',
            'lengthOfRecordings',
            'codec',)