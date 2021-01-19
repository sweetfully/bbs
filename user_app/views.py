from django.shortcuts import render, HttpResponse

from user_app import models
from utils.result_dict_util import ResultDict
from utils.tmp_util import get_random_by_len
from user_app.models import UserInfo
from user_app.forms import RegisterForm
from geetest import GeetestLib
from configs import geetest_config
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
    if request.method == "POST":
        login_name = request.POST.get("username")
        password = request.POST.get("password")
        print(login_name, password)
        print("*" * 120)
        if not len(login_name):
            return ResultDict.get_error_response("用户名不能为空!")
        if not len(password):
            return ResultDict.get_error_response("密码不能为空!")
        result = is_username(login_name)
        if result == None:
            return ResultDict.get_error_response("输入的用户名既不是用户ID也不是手机号！")
        else:
            if result:
                user = auth.authenticate(request, username=login_name, password=password)
                print("user对象:", user.username,user.password)
            else:
                print(login_name)
                user = auth.authenticate(request, phone=login_name, password=password)
                print()
            if user:
                auth.login(request, user=user)
                return ResultDict.get_success_response("/home/")
            else:
                return ResultDict.get_error_response("用户名或密码错误")
    return render(request, "login.html")


def register(request):
    print(request.method.center(80, '-'))
    if request.method == "POST":
        validate_result = pc_ajax_validate(request)
        if validate_result:  # 通过了验证码的验证
            reg_form_obj = RegisterForm(request.POST)
            print(request.POST)
            if reg_form_obj.is_valid():

                password = request.POST.get("password")
                reg_form_obj.cleaned_data.pop("re_password")
                if request.POST.get("phone").strip() == "":
                    reg_form_obj.cleaned_data.pop("phone")

                avatar = request.FILES.get("avatar")
                print("头像：", avatar)
                # todo   生成的随机用户名需要去验证
                username = "ID" + get_random_by_len(6)
                print("username", username)
                data = models.UserInfo.objects.filter(username=username)
                if data:
                    return ResultDict.get_error_response("用户ID重复")
                else:
                    pass

                UserInfo.objects.create_user(**reg_form_obj.cleaned_data, avatar=avatar, username=username)
                user = auth.authenticate(request, username=username, password=password)
                auth.login(request, user=user)
                return ResultDict.get_success_response("/home/")
            else:
                return ResultDict.get_error_response(reg_form_obj.errors)
        else:    # 验证码没通过
            return ResultDict.get_error_response("验证码有误")
    return render(request, "register.html", {"forms": RegisterForm()})


def pc_get_captcha(request):
    user_id = 'test'
    gt = GeetestLib(geetest_config.pc_geetest_id, geetest_config.pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def pc_ajax_validate(request):
    gt = GeetestLib(geetest_config.pc_geetest_id, geetest_config.pc_geetest_key)
    challenge = request.POST.get(gt.FN_CHALLENGE, '')
    validate = request.POST.get(gt.FN_VALIDATE, '')
    seccode = request.POST.get(gt.FN_SECCODE, '')
    status = request.session[gt.GT_STATUS_SESSION_KEY]
    user_id = request.session["user_id"]
    if status:
        result = gt.success_validate(challenge, validate, seccode, user_id)
    else:
        result = gt.failback_validate(challenge, validate, seccode)
    return result
