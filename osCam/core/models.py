#core/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json as JSON

class Recording(models.Model):
    #recordedOn = models.DateTimeField(auto_now_add=True)
    recordingLength = models.IntegerField(blank=True, null=True)
    fileName = models.CharField(max_length=40, blank=True, null=True)
    filePath = models.CharField(max_length=40, blank=True, null=True)
    cameraId = models.ForeignKey("userconfig.Camera", on_delete=models.CASCADE, blank=True, null=True)
    # def __str__(self) -> str:
    #     return self.fileName
    def __str__(self) -> str:
            return JSON.dumps({"recordingLength":self.recordingLength, "fileName":self.fileName, 
            "filePath": self.filePath, "cameraId": self.cameraId})

