from django.contrib import admin
from .models import CameraView, Camera, Storage

admin.site.register(Camera)
admin.site.register(CameraView)
admin.site.register(Storage)
