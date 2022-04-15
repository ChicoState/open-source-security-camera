from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Network)
admin.site.register(RaspberryPi)
admin.site.register(Camera)
admin.site.register(CameraView)
admin.site.register(Storage)