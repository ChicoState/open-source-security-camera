"""osCam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from unicodedata import name
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
# from core import views as core_views
# from user import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns #helper for returning URL of which SERVES up static files
import streamin
import userconfig as user_config

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls'), name='core'),
    path('', include('user.urls'), name='onboarding'),
    path('settings/', include('userconfig.urls'), name='settings'),
    path('stream/', include('streamin.urls'), name='stream'),
]

# Serves up files to server in Developemnt Mode
if settings.DEBUG:
    print("\n\n[DEBUG] OsCammode.is_on() == True\n", "%%%"*75)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
# Media.____
# only dev
# for our production server we would need to do differently..
# if we want to serve videos up somewhere we would use that media path (similar to Google.Static)