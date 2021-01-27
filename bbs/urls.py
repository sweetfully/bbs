"""bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views import static
from django.views.static import serve
from django.urls import path, include
from user_app import urls as user_urls
from bbs import views, settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(user_urls)),
    path('home/', views.home, name='bbs_home'),
    path('home2/', views.home2, name='bbs_home2'),
    url('^$', views.index),
    url(r'^avatars/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    url('phb_list/', views.phb_list),
    # url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]

# 错误页面路径配置
handler404 = views.page_not_found
