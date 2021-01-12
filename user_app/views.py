from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib import auth

# Create your views here.


def is_username(name):
    '''
    判断用户名是否是用户名，返回Ture表示是用户名，返回False表示是手机号
    :param name:
    :return:
    '''
    if len(name) == 11:
        return False
    if name.startswith("ID"):
        return True
    return None


def login(request):
    if request.method == "post":
        login_name = request.POST.get("username")
        password = request.POST.get("password")
        if len(login_name):
            return JsonResponse({"status": 1, "msg": "用户名不能为空!"})
        if len(password):
            return JsonResponse({"status": 1, "msg": "密码不能为空!"})
        result = is_username(login_name)
        if result == None:
            return JsonResponse({"status": 1, "msg": "输入的用户名既不是用户ID也不是手机号！"})
        else:
            if request:
                pass
            else:
                pass
    return render(request, "login.html")
