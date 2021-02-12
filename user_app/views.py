from django.shortcuts import render, HttpResponse, redirect

from utils.result_dict_util import ResultDict
from utils.tmp_util import get_random_by_len
from user_app.models import UserInfo
from user_app.forms import RegisterForm
from geetest import GeetestLib
from configs import geetest_config
from django.contrib import auth
from bbs.settings import LOGIN_URL

# Create your views here.


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
        user = auth.authenticate(request, username=login_name, password=password)
        # print("user对象:", user.username, user.password)
        if user:
            auth.login(request, user=user)
            return ResultDict.get_success_response("/home/")
        else:
            return ResultDict.get_error_response("用户名或密码错误")
    return render(request, "login.html")


def register(request):
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

                while(True):
                    username = "ID" + get_random_by_len(6)
                    print("username", username)
                    data = UserInfo.objects.filter(username=username)
                    if not data:
                        break

                avatar = request.FILES.get("avatar")
                print("头像：", avatar)
                if avatar:
                    UserInfo.objects.create_user(**reg_form_obj.cleaned_data, avatar=avatar, username=username)
                else:
                    UserInfo.objects.create_user(**reg_form_obj.cleaned_data, username=username)

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


def get_user_data(request):
    print(request.path)
    return render(request, "person_information.html")


def account_safe_set(request):
    return render(request, "account_safe.html")


def logout(request):
    auth.logout(request)
    return redirect(LOGIN_URL)
