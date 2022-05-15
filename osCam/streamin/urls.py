
# from msilib.schema import Media
from django.urls import path
from . import views


TYPE="stream"

urlpatterns = [
    path('', views.view_gallery_stream, name=f'gallery-{TYPE}'),
    path('add/', views.CreateVideo.as_view(), name=f"create-{TYPE}"),

    path('detail/<int:pk>/', views.DetailView.as_view(), name=f'{TYPE}-detail'),

    # path('add/', views.DetailView.as_view(), name=f"create-{TYPE}"),
    path('edit/<int:id>/', views.UpdateVideo.as_view(), name=f"{TYPE}-update"),
    path('remove/<int:id>/', views.DeleteVideo.as_view(), name=f"{TYPE}-delete"),
] 