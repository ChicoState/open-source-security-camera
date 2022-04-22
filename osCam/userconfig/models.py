from typing_extensions import Required
from urllib import request
from django.db import models
from django.contrib.auth.models import User


class Network(models.Model):
    home_ip_address = models.CharField(max_length=32, null=True, blank=True)
    camera_ip_address = models.CharField(max_length=32, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


class RaspberryPi(models.Model):
    # User can have Many RaspberryPie (1:Many)
    user = models.ForeignKey( User, on_delete=models.CASCADE, null=True, blank=True )
    network = models.ForeignKey(Network, on_delete=models.DO_NOTHING, null=True, blank=True)
    model_num = models.IntegerField(blank=True, null=True)
    model_name = models.CharField(max_length=40,blank=True, null=True)
    username = models.CharField(max_length=40, default='admin')
    password = models.CharField(max_length=40, default='admin')


class Camera(models.Model):
    # Rasberry Pi can have Many Camera (1:Many)
    user = models.ForeignKey( User, on_delete=models.CASCADE, null=True, blank=True )
    raspberry_pi = models.ForeignKey( RaspberryPi , on_delete=models.CASCADE, null=True, blank=True)
    model_num = models.IntegerField(blank=True, null=True)
    model_name = models.CharField(max_length=40,blank=True, null=True)
<<<<<<< HEAD
    camera_index = models.IntegerField(default=0)
=======
    camera_index = models.IntegerField(default=0, unique=False, editable=False)
>>>>>>> d18ffbc (Enhanced Camera view/feed forms. Changed all the config pages to just one Settings page.)
    device_name = models.CharField(max_length=40, default='Camera')
    ip_address = models.CharField(max_length=40, default='10.0.0.94')
    port = models.IntegerField(default=80)


class camera_view(models.Model):
    show_motion_boxes = models.BooleanField(default=False)
    show_contours = models.BooleanField(default=False)
    show_text = models.BooleanField(default=False)
    text = models.CharField(max_length=255, default='Cam Name :: Date :: Time')
    contrast = models.IntegerField(default=0)
    brightness = models.IntegerField(default=0)
    recording = models.BooleanField(default=False, blank=True, null=True)
    fps = models.IntegerField(default=15)
    invert = models.BooleanField(default=False)
    mirror = models.BooleanField(default=False)


class Storage(models.Model):
    record_to_device = models.BooleanField(default=False)
    record_to_cloud = models.BooleanField(default=False)
    file_path = models.CharField(max_length=255, default='/home/pi/Videos')
    max_space = models.IntegerField(default=0)
    time_to_live = models.IntegerField(default=0)
    archive = models.BooleanField(default=False)
    length_of_recordings = models.IntegerField(default=0)
    codec = models.CharField(max_length=40, default='h264') 