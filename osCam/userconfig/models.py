from typing_extensions import Required
from urllib import request
from django.db import models
from user.models import CustomUser

class Network(models.Model):
    homeIpAddress = models.CharField(max_length=32, null=True, blank=True)
    homeNetmask = models.CharField(max_length=32, null=True, blank=True)
    cameraIpAddress = models.CharField(max_length=32, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.homeIpAddress

class RaspberryPi(models.Model):
    # User can have Many RaspberryPie (1:Many)
    user = models.ForeignKey( CustomUser, on_delete=models.CASCADE, null=True, blank=True )
    #network can have many RaspberryPie (1:Many) (we could do manyToMany but assuming we're coding MVP model)
    network = models.ForeignKey(Network, on_delete=models.DO_NOTHING, null=True, blank=True)
    modelNum = models.IntegerField(blank=True, null=True)
    modelName = models.CharField(max_length=40,blank=True, null=True)
    username = models.CharField(max_length=40, default='admin')
    password = models.CharField(max_length=40, default='admin')

    def __str__(self):
        return self.modelName

class Camera(models.Model):
    user = models.ForeignKey( CustomUser, on_delete=models.CASCADE, null=True, blank=True )
    raspberryPi = models.ForeignKey( RaspberryPi , on_delete=models.CASCADE, null=True, blank=True)
    modelNum = models.IntegerField(blank=True, null=True)
    modelName = models.CharField(max_length=40,blank=True, null=True)
    cameraIndex = models.IntegerField(default=0, unique=False, editable=False)
    deviceName = models.CharField(max_length=40, default='Camera 01')
    ipAddress = models.CharField(max_length=40, default='10.0.0.94')
    port = models.IntegerField(default=80)

    def __str__(self):
        return self.deviceName

class CameraView(models.Model):
    user = models.ForeignKey( CustomUser, on_delete=models.CASCADE, null=True, blank=True )
    # camera = models.ForeignKey( Camera, on_delete=models.CASCADE, null=True, blank=True)
    showMotionBoxes = models.BooleanField(default=False)
    showContours = models.BooleanField(default=False)
    showText = models.BooleanField(default=False)
    text = models.CharField(max_length=255, default='Cam Name :: Date :: Time')
    contrast = models.IntegerField(default=0, blank=True, null=True)
    brightness = models.IntegerField(default=0, blank=True, null=True)
    recording = models.BooleanField(default=False, blank=True, null=True)
    fps = models.IntegerField(default=15)
    invert = models.BooleanField(default=False)
    mirror = models.BooleanField(default=False)

    def __str__(self):
        return "Camera View settings"

class Storage(models.Model):
    recordToDevice = models.BooleanField(default=False)
    recordToCloud = models.BooleanField(default=False)
    filePath = models.CharField(max_length=255, default='/home/pi/Videos')
    maxSpace = models.IntegerField(default=0, blank=True, null=True)
    timeToLive = models.IntegerField(default=0, blank=True, null=True)
    archive = models.BooleanField(default=False, blank=True, null=True)
    lengthOfRecordings = models.IntegerField(default=0, blank=True, null=True)
    codec = models.CharField(max_length=40, default='h264')

    def __str__(self):
        return self.filePath
