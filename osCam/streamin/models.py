from dataclasses import dataclass
from pydoc import describe
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

# Default Video path will be stored in Media/Uploads/video_storage with a img thumbnail created by the open CV library
class Video(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default="Anonymous", null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to="uploads/video_storage", validators=[FileExtensionValidator(allowed_extensions=['mp4','.avi'])])
    thumbnail = models.FileField(upload_to="uploads/thumbnails", validators=[FileExtensionValidator(allowed_extensions=['png','jpg', 'jpeg', 'svg'])])
    data_created = models.DateTimeField(default=timezone.now)