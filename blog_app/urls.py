from django.urls import path, re_path
from blog_app import views

urlpatterns = [
    re_path('^(?P<username>ID[0-9]{6})/home/$', views.get_blog_home),
    path('blog_list/', views.get_blog_list_by_username),
    path('message_manager/', views.message_manager_list),
    path('favorite_dir/', views.get_favorite_dir),
    path('favorite_list/', views.get_favorite_list),
    path('write_blog/', views.write_blog),
]