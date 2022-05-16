from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    emailKey = models.CharField(max_length=16, blank=True)


class Camera(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    deviceName = models.CharField(
        max_length=40,
        default='Camera 01'
    )

    def __str__(self):
        return self.deviceName


class CameraView(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    camera = models.ForeignKey(
        Camera,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    showMotionBoxes = models.BooleanField(default=False)
    showText = models.BooleanField(default=False)
    text = models.CharField(max_length=255, default='Cam Name :: Date :: Time')
    fps = models.IntegerField(default=15)
    invert = models.BooleanField(default=False)
    mirror = models.BooleanField(default=False)
    scale = models.DecimalField(max_digits=3, decimal_places=2, default=0.75)

    def __str__(self):
        return "Camera View settings"


class Storage(models.Model):
    recordToDevice = models.BooleanField(default=False)
    filePath = models.CharField(max_length=255, default='/home/pi/Videos')
    maxSpace = models.IntegerField(default=0, blank=True, null=True)
    timeToLive = models.IntegerField(default=0, blank=True, null=True)
    lengthOfRecordings = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.filePath