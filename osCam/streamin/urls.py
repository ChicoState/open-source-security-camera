from django.urls import path
from . import views

TYPE="stream"

urlpatterns = [
    path('', views.videoStreamGallery, name=f'gallery-{TYPE}'),
    path('add/', views.addStream, name=f"add-{TYPE}"),
    path('edit/<int:id>/', views.editStream, name=f"edit-{TYPE}"),
    path('remove/<int:id>/', views.removeStream, name=f"remove-{TYPE}"),
]
