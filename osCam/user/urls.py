from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # path('', views.taskPage, name="task_page"),
    path('join/', views.join, name='join'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),

] 
    