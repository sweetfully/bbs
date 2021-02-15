from django.shortcuts import render
from user_app import models as user_models
from blog_app import models as blog_models

# Create your views here.


def get_blog_home(request, username):
    print("username：", username)
    user_set = user_models.UserInfo.objects.filter(username=username).values("id", "username", "email", "date_joined",
                                                                "user_nick", "phone", "avatar", "user_info")
    print(len(user_set))
    if len(user_set):
        blog_set = blog_models.Blog.objects.filter(publisher__username=username)
        print(len(blog_set), blog_set)
        return render(request, "blog_home.html", {"user": user_set[0], "blog_contents": blog_set})
    return render(request, "error.html")


def message_manager_list(request):
    return render(request, "message_manager.html")
