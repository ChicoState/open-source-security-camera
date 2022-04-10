from urllib import request
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
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

class Camera(models.Model):
    # Rasberry Pi can have Many Camera (1:Many)
    user = models.ForeignKey( User, on_delete=models.CASCADE, null=True, blank=True )
    raspberry_pi = models.ForeignKey( RaspberryPi , on_delete=models.CASCADE, null=True, blank=True)
    model_num = models.IntegerField(blank=True, null=True)
    model_name = models.CharField(max_length=40,blank=True, null=True)
