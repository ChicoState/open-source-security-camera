from django.urls import path
from . import views

TYPE = "stream"

urlpatterns = [
    path('', views.view_gallery_stream, name=f'gallery-{TYPE}'),
    path('add/', views.CreateVideo.as_view(), name=f"create-{TYPE}"),
    path('edit/<int:pk>/', views.video_stream_edit, name=f"{TYPE}-update"),
    path('remove/<int:pk>/', views.DeleteVideo.as_view(), name=f"{TYPE}-delete"),
] 