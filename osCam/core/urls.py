
from django.urls import path
from . import views

# Use if you find yourself prefexing or
# postfixing to 'path/' or
# name='some_{name}'
# global TYPE="stream"

urlpatterns = [
    path('', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
]
