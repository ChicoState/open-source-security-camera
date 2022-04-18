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

class NextPath(models.Model):
    data = models.CharField(default="", max_length=500, blank=True, null=True)
    # path = models.ForeignKey(Path, on_delete=models.CASCADE, blank=True, null=True)

class Path(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    path = models.CharField(default='/', max_length=500,blank=True, null=True)
    next = models.ForeignKey(NextPath, on_delete=models.CASCADE, blank=True, null=True)



