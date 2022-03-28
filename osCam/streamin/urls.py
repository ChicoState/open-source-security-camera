
from django.urls import path
from . import views

TYPE="stream"

urlpatterns = [
    path('', views.view_stream, name=f'{TYPE}-page'),
    path('add/', views.add_stream, name=f"add-{TYPE}"),
    path('edit/<int:id>/', views.edit_stream, name=f"edit-{TYPE}"),
    path('remove/<int:id>/', views.remove_stream, name=f"remove-{TYPE}"),
] 