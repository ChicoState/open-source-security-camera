from django.contrib import admin
from .models import Network, RaspberryPi, Camera
# Register your models here.
admin.site.register(Network)
admin.site.register(RaspberryPi)
admin.site.register(Camera)