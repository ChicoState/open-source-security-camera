#core/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
<<<<<<< HEAD
import json as JSON

class Recording(models.Model):
    #recordedOn = models.DateTimeField(auto_now_add=True)
    recordingLength = models.IntegerField(blank=True, null=True)
    fileName = models.CharField(max_length=40, blank=True, null=True)
    filePath = models.CharField(max_length=40, blank=True, null=True)
    cameraId = models.ForeignKey("userconfig.Camera", on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self) -> str:
        return self.fileName
    # def __str__(self) -> str:
    #         return JSON.dumps({"recordingLength":self.recordingLength, "fileName":self.fileName, 
    #         "filePath": self.filePath, "cameraId": self.cameraId})

class StorageHandler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    update = models.BooleanField(default=False)
    fullpath = models.CharField(max_length=500,blank=True, null=True)
    def __str__(self) -> str:
        return "StorageHandler {} in-use? {}".format(self.id, self.update)

class NextPath(models.Model):
    data = models.CharField(default="", max_length=500, blank=True, null=True)
    # path = models.ForeignKey(Path, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self) -> str:
        return self.data
    # def __str__(self) -> str:
    #     return JSON.dumps({"data":self.data})

class Path(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    path = models.CharField(default='/', max_length=500,blank=True, null=True)
    next = models.ForeignKey(NextPath, on_delete=models.CASCADE, blank=True, null=True)
    storage = models.ForeignKey(StorageHandler, on_delete=models.DO_NOTHING, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.path
    # def __str__(self) -> str:
    #     obj = {"user":self.user.username, "path":self.path, "next":self.next}
    #     return JSON.dumps(obj)



=======
from django.utils.translation import activate
>>>>>>> f78c4c4 (Adding configuration page, added variables in models for Camera setup.)
