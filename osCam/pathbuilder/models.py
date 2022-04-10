from django.db import models
from django.contrib.admin.models import User

class StorageHandler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    update = models.BooleanField(default=False)
    fullpath = models.CharField(max_length=500,blank=True, null=True)
    def __str__(self) -> str:
        return "StorageHandler {} in-use? {}".format(self.id, self.update)



# from django.utils.translation import activate


# Create your models here.
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

