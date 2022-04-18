import imp
from django.contrib import admin
from .models import StorageHandler
from .models import NextPath, Path, Recording

# Register your models here.
admin.site.register(Recording)
admin.site.register(Path)
admin.site.register(NextPath)
admin.site.register(StorageHandler)
