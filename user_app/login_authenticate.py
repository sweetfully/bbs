from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from user_app.models import UserInfo


class UsernameMobileAuthBackend(ModelBackend):
    """用户名或手机登录"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """判断用户名(手机号码)和密码是否正确"""
        print(username, password)
        query_set = UserInfo.objects.filter((Q(username=username) | Q(phone=username)))
        try:
            if query_set.exists():
                user = query_set.get()
                if user.check_password(password):
                    return user
        except:
            return None
        return None
