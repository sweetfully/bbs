from enum import Enum
from django.http import JsonResponse


class Status(Enum):
    SUCCESS = 200
    ERROR = 1
    NEED_LOGIN = 10


class ResultDict():
    def __init__(self, status, msg, data=""):
        self.status = status
        self.msg = msg
        self.data = data

    @staticmethod
    def get_success_response(data=""):
        return ResultDict(Status.SUCCESS.value, "ok", data).__to_json_response()
    
    @staticmethod
    def get_error_response(msg, data=""):
        return ResultDict(Status.ERROR.value, msg, data).__to_json_response()

    @staticmethod
    def get_need_login_response(data=""):
        return ResultDict(Status.NEED_LOGIN.value, "请登录", data).__to_json_response()

    def __to_json_response(self):
        ret = {"status": self.status, "msg": self.msg}
        if self.data:
            ret["data"] = self.data
        return JsonResponse(ret)