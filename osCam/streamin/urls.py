from django.urls import path
from . import views

TYPE = "stream"

urlpatterns = [
    path('', views.view_gallery_stream, name=f'gallery-{TYPE}'),
    path('edit/<int:pk>/', views.video_stream_edit, name=f"{TYPE}-update"),
    path('remove/<int:pk>/', views.removeStream, name=f"{TYPE}-delete"),
] 