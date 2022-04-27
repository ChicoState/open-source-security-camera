from django.db import models
from user.models import CustomUser

class PathBuilderHandler(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    update = models.BooleanField(default=False)
    fullpath = models.CharField(max_length=500,blank=True, null=True)
    def __str__(self) -> str:
        return "{ update_rule:{} , media_path:{} }".format(self.update, self.update)

class NextPath(models.Model):
    data = models.CharField(default="", max_length=500, blank=True, null=True)
    def __str__(self) -> str:
        return self.data

class Path(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    path = models.CharField(default='/', max_length=500,blank=True, null=True)
    next = models.ForeignKey(NextPath, on_delete=models.CASCADE, blank=True, null=True)
    storage = models.ForeignKey(PathBuilderHandler, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self) -> str:
        return self.path
