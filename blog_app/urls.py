from django.urls import path, re_path
from blog_app import views

urlpatterns = [
    re_path('^(?P<username>ID[0-9]{6})/home/$', views.get_blog_home),
]