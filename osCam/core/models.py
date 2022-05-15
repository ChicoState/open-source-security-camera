#core/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Recording(models.Model):
    #recordedOn = models.DateTimeField(auto_now_add=True)
    recordingLength = models.IntegerField(blank=True, null=True)
    fileName = models.CharField(max_length=40, blank=True, null=True)
    filePath = models.CharField(max_length=40, blank=True, null=True)
    cameraId = models.ForeignKey("userconfig.Camera", on_delete=models.CASCADE, blank=True, null=True)



