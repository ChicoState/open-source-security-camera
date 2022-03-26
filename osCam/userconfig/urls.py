from django.urls import path
from . import views


urlpatterns = [
        path('', views.configPage, name="config-page"),
    path('add/', views.addConf, name="add-config"),
    path('edit/<int:id>/', views.editConf, name="edit-config"),
    path('remove/<int:id>/', views.removeConf, name="remove-config"),
] 

