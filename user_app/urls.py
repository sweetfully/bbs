from django.urls import path, re_path
from user_app import views

urlpatterns = [
    path('login/', views.login)
]