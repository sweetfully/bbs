from django.shortcuts import render

from utils.result_dict_util import ResultDict


def home(request):
    print(request.user.user_nick)
    return ResultDict.get_success_response("欢迎回来：" + request.user.user_nick)