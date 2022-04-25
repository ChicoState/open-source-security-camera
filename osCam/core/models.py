#core/models.py
from django.db import models

class Recording(models.Model):
    recordingLength = models.IntegerField(blank=True, null=True)
    fileName = models.CharField(max_length=40, blank=True, null=True)
    filePath = models.CharField(max_length=40, blank=True, null=True)
    cameraId = models.ForeignKey("userconfig.Camera", on_delete=models.CASCADE, blank=True, null=True)
    