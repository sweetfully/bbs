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
    user_nick = FixedCharField(max_length=30)
    phone = models.CharField(max_length=11, unique=True, db_index=True, null=False)
    avatar = FixedCharField(max_length=50, default='/img/default.png')


