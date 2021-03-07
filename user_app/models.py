from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class FixedCharField(models.Field):
    def __init__(self, max_length, *args, **kwargs):
        super().__init__(max_length=max_length, *args, **kwargs)
        self.length = max_length

    def db_type(self, connection):
        return "char(%s)" % self.length


class UserInfo(AbstractUser):
    user_nick = models.CharField(max_length=30)
    phone = FixedCharField(max_length=11, unique=True, db_index=True, null=True)
    avatar = models.FileField(upload_to='avatars', default='/avatars/default.png')
    user_info = models.CharField(max_length=200, null=True)
    focus = models.ManyToManyField(to='UserInfo', through='Focus')
    detail_info = models.OneToOneField(to="UserDetailInfo", on_delete=models.CASCADE)


# 用户的详细信息表
class UserDetailInfo(models.Model):
    age = models.IntegerField(default=0)
    sex = models.BooleanField(default=True)
    birthday = models.DateField(default='2010-01-01')
    hometown = models.CharField(max_length=50, null=False)


# 关注表
class Focus(models.Model):
    # id
    # 关注人    ->    user表
    # 被关注人    ->    user表
    # 关注时间
    focus_id = models.AutoField(primary_key=True)
    focus_people = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE, related_name='follow_user')
    be_focus_people = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE, related_name='follow_me_user')
    focus_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('focus_people', 'be_focus_people')


