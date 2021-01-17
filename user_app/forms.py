'''
bbs项目注册模块的form类
'''

from django import forms
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    user_nick = forms.CharField(
        max_length=30,
        label="昵称：",
        widget=forms.widgets.TextInput(attrs={"class": "form-control", "autocomplete": "off"}),
        error_messages={"max_length": "昵称最长为30位", "required": "昵称不能为空"},
    )

    password = forms.CharField(
        max_length=20,
        min_length=6,
        label="密码：",
        widget=forms.widgets.PasswordInput(attrs={"class": "form-control"}),
        error_messages={"max_length": "密码最长30位", "min_length": "密码最少6位", "required": "密码不能为空"},
    )

    re_password = forms.CharField(
        max_length=20,
        min_length=6,
        label="确认密码：",
        widget=forms.widgets.PasswordInput(attrs={"class": "form-control"}),
        error_messages={"max_length": "密码最长30位", "min_length": "密码最少6位", "required": "密码不能为空"},
    )

    email = forms.EmailField(
        label="邮箱（可选）：",
        widget=forms.widgets.EmailInput(attrs={"class": "form-control", "autocomplete": "off"}),
        required=False,
        error_messages={"invalid": "邮箱格式不正确"},
    )

    phone = forms.CharField(
        min_length=11,
        max_length=11,
        required=False,
        label="电话（可选）：",
        widget=forms.widgets.TextInput(attrs={"class": "form-control", "autocomplete": "off"}),
        error_messages={"max_length": "手机号是11位", "min_length": "手机号是11位"},
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        if pwd.isdigit() or pwd.isalpha():
            self.add_error('password', ValidationError("密码必须包含数字和字母"))
        else:
            return self.cleaned_data.get('password')

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd == re_pwd:
            return self.cleaned_data
        else:
            self.add_error('re_password', ValidationError("两次输入的密码不一致"))
