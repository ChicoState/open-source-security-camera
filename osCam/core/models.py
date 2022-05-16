from time import strftime
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

class Recording(models.Model):
    recordingLength = models.IntegerField(
        blank=True,
        null=True
    )
    fileName = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )
    filePath = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )
    cameraId = models.ForeignKey(
        "userconfig.Camera",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    
    title = models.CharField(max_length=255, blank=True, null=True) 
    description = models.TextField(default="")
    video_file = models.FileField(upload_to='uploads/video_storage/%Y/%m/%d/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['mp4','.avi'])])
    thumbnail = models.FileField(upload_to='uploads/thumbnails/%Y/%m/%d/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['png','jpg', 'jpeg', 'svg'])])
    data_created = models.DateTimeField(default=timezone.now)

    def parse_dir_by_date(self):
        """helper to parse/retrieve location media content for view consumption. """
        return 'uploads/video_storage/{}/{}/{}/'.format(strftime("/%Y/%m/%d"))
