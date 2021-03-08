from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from utils.result_dict_util import ResultDict
from utils.tmp_util import get_random_by_len
from utils import date_util
from utils import sql_result_util
from user_app.models import UserInfo, Focus, UserDetailInfo
from user_app.forms import RegisterForm
from geetest import GeetestLib
from configs import geetest_config
from bbs.settings import LOGIN_URL

FOCUS_NUM_BY_PAGE = 5


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
                user_detail_info = UserDetailInfo.objects.create()
                if avatar:
                    UserInfo.objects.create_user(**reg_form_obj.cleaned_data, avatar=avatar, username=username,
                                                 detail_info=user_detail_info)
                else:
                    UserInfo.objects.create_user(**reg_form_obj.cleaned_data, username=username,
                                                 detail_info=user_detail_info)

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


def set_attention_user(request):
    if not request.user.is_authenticated:
        return ResultDict.get_need_login_response()
    be_focus_user_id = getattr(request, request.method).get('userId')
    operate = int(getattr(request, request.method).get('operate'))
    print(be_focus_user_id, operate)
    if not be_focus_user_id:
        return ResultDict.get_error_response("关注人的用户ID不能为空!")
    if be_focus_user_id == str(request.user.id):
        return ResultDict.get_error_response("自己不能关注自己!")
    be_focus_user = UserInfo.objects.get(id=be_focus_user_id)
    if not be_focus_user:
        return ResultDict.get_error_response("此用户ID不正确!")
    focus_result = Focus.objects.filter(focus_people=request.user, be_focus_people=be_focus_user)
    if operate == 1:
        if focus_result:
            return ResultDict.get_error_response("该用户您已经关注了!")
        else:
            focus_result = Focus.objects.create(focus_people=request.user, be_focus_people=be_focus_user)
            if focus_result:
                return ResultDict.get_success_response("关注成功!")
            else:
                return ResultDict.get_error_response("发生了异常，关注失败!")
    elif operate == 2:
        if focus_result:
            focus_result.first().delete()
            return ResultDict.get_success_response("取消关注成功!")
        else:
            return ResultDict.get_error_response("您还未关注该用户!")
    return ResultDict.get_error_response("operate参数不正确！")


def get_attention_user_list(request):
    if request.user.is_authenticated:
        current_user_id = request.user.id
    else:
        current_user_id = -1     # 数据库中的主键是不会为-1的
    user_id = getattr(request, request.method).get('userId')
    attention_type = int(getattr(request, request.method).get('type'))
    page = int(getattr(request, request.method).get('page'))
    print("user_id:", user_id, "; attention_type:", attention_type, "; page:", page)
    if not user_id:
        return ResultDict.get_error_response("用户ID不能为空!")
    user = UserInfo.objects.get(id=user_id)
    if not user:
        return ResultDict.get_error_response("此用户ID不正确!")
    start_focus_position = (page - 1) * FOCUS_NUM_BY_PAGE
    if attention_type == 1:
        sql = """SELECT c.focus_id, c.focus_time, b.id, b.username, b.user_nick, b.user_info, b.avatar, 
            (select count(1) FROM user_app_focus WHERE focus_people_id = %s and be_focus_people_id = b.id) is_focus 
            FROM  user_app_userinfo a, user_app_userinfo b, user_app_focus c 
            WHERE c.focus_people_id = a.id and c.be_focus_people_id = b.id 
            and c.focus_people_id = %s 
            ORDER BY b.user_nick DESC LIMIT %s, %s"""
        params = (current_user_id, user_id, start_focus_position, FOCUS_NUM_BY_PAGE)
    elif attention_type == 2:
        sql = """SELECT c.focus_id, c.focus_time, b.id, b.username, b.user_nick, b.user_info, b.avatar, 
            (select count(1) FROM user_app_focus WHERE focus_people_id = %s and be_focus_people_id = b.id) is_focus 
            FROM  user_app_userinfo a, user_app_userinfo b, user_app_focus c 
            WHERE c.be_focus_people_id = a.id and c.focus_people_id = b.id 
            and c.be_focus_people_id = %s 
            ORDER BY b.user_nick DESC LIMIT %s, %s"""
        params = (current_user_id, user_id, start_focus_position, FOCUS_NUM_BY_PAGE)
    elif attention_type == 3:
        sql = """SELECT a.focus_id, a.focus_time, c.id, c.username, c.user_nick, c.user_info, c.avatar, 
            (select count(1) FROM user_app_focus WHERE focus_people_id = %s and be_focus_people_id = c.id) is_focus 
            FROM user_app_focus a, user_app_focus b, user_app_userinfo c 
            WHERE a.focus_people_id = b.be_focus_people_id 
            and a.be_focus_people_id = b.focus_people_id 
            and a.focus_people_id = %s and a.be_focus_people_id = c.id 
            ORDER BY c.`user_nick` DESC limit %s, %s"""
        params = [current_user_id, user_id, start_focus_position, FOCUS_NUM_BY_PAGE]
    else:
        return ResultDict.get_error_response("type类型不正确")
    focus_list = Focus.objects.raw(sql, params=params)
    focus_dict_list = sql_result_util.result_to_list(focus_list)
    return ResultDict.get_success_response(focus_dict_list)


@login_required
def get_user_data(request):
    blog_age = date_util.get_date_interval(request.user.date_joined)
    return render(request, "person_information.html", {"blog_age": blog_age})


@login_required
def change_avatar(request):
    avatar = request.FILES.get("avatar")
    print("头像：", avatar)
    if avatar:
        try:
            request.user.avatar = avatar
            request.user.save()
        except Exception:
            return ResultDict.get_error_response("头像更新失败")
        return ResultDict.get_success_response(str(request.user.avatar))
    else:
        ResultDict.get_error_response("没有传递头像信息")


@login_required
def change_user_info(request):
    nickname = request.POST.get("nickname")
    age = request.POST.get("age")
    sex = request.POST.get("sex")
    birthday = request.POST.get("birthday")
    hometown = request.POST.get("hometown")
    user_info = request.POST.get("userInfo")
    if nickname:
        request.user.user_nick = nickname
        request.user.detail_info.age = age
        request.user.detail_info.sex = sex
        request.user.detail_info.birthday = birthday
        request.user.detail_info.hometown = hometown
        request.user.user_info = user_info
        request.user.detail_info.save()
        request.user.save()
        # 生成一个对象，用于前端重新更新值
        dic = dict()
        dic["username"] = request.user.username
        dic["user_nick"] = request.user.user_nick
        dic["age"] = request.user.detail_info.age
        dic["sex"] = request.user.detail_info.sex
        dic["birthday"] = request.user.detail_info.birthday
        dic["hometown"] = request.user.detail_info.hometown
        dic["user_info"] = request.user.user_info
        return ResultDict.get_success_response(dic)
    else:
        return ResultDict.get_error_response("用户昵称不能为空")


def account_safe_set(request):
    return render(request, "account_safe.html")


def logout(request):
    auth.logout(request)
    return redirect(LOGIN_URL)
