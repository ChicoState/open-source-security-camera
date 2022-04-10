#core/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import activate

class Recording(models.Model):
    recorded_on = models.DateTimeField(auto_now_add=True)
    recording_length = models.IntegerField(blank=True, null=True)
    camera_id = models.ForeignKey("userconfig.Camera", on_delete=models.CASCADE, blank=True, null=True)
