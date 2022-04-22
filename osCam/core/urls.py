
from django.urls import path
from . import views

# Use if you find yourself prefexing or postfixing to 'path/' or name='some_{name}'
# global TYPE="stream"

urlpatterns = [
    path('', views.home, name='home'),   
    # path('<str>/',views.getFilePath, name='filepath') ,
    path('feed/', views.feed, name='feed'),
    # path('/settings/', views.settings, name='settings'),
]
