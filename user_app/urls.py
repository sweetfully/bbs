from django.urls import path, re_path
from user_app import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('logout', views.logout),
    path('get_captcha/', views.pc_get_captcha),
    path('like_or_no_user/', views.set_attention_user),
    path('like_list/', views.get_attention_user_list),
    path('user_data/', views.get_user_data),
    path('account_safe/', views.account_safe_set),
]