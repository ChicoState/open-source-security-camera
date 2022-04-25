from django.contrib import admin
from .models import PathBuilderHandler, NextPath, Path

# Register your models here.
admin.site.register(Path)
admin.site.register(NextPath)
admin.site.register(PathBuilderHandler)