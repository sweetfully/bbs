from math import ceil

from django.db.models import Count
from django.shortcuts import render, redirect
from blog_app import models as blog_model
from utils.result_dict_util import ResultDict
from utils import sql_result_util
from django.urls import reverse

every_page_content_num = 5


def home(request):
    # 得到请求链接中page的值，如果没值设置默认值1
    page = int(getattr(request, request.method).get('page', 1))
    # 计算当前页的第一条记录
    start_num = (page - 1) * every_page_content_num
    # 计算当前页的最后一条记录
    end_num = page * every_page_content_num
    # limit限制取数
    blog_contents = blog_model.Blog.objects.all()[start_num:end_num]
    # 总页数（向上取整）
    num_pages = ceil(blog_model.Blog.objects.count() / every_page_content_num)
    # 如果没有数据，不显示分页组件和列表
    if num_pages == 0:
        return render(request, "index.html")
    else:
        return render(request, "index.html", {"blog_contents": blog_contents, "current_num": page, "num_pages": num_pages})


def recommend_list(request):
    recommend_type = int(getattr(request, request.method).get('type', 1))
    recommend_num = 5
    if recommend_type == 1:
        list_data_set = blog_model.Blog.objects.raw(
            "select count(1) as count, user_app_userinfo.id, user_app_userinfo.username,"
            " user_app_userinfo.user_nick, user_app_userinfo.user_info, user_app_userinfo.avatar"
            " from user_app_focus LEFT JOIN user_app_userinfo on user_app_focus.be_focus_people_id = user_app_userinfo.id"
            " GROUP BY user_app_focus.be_focus_people_id ORDER BY count DESC LIMIT %s", params=[recommend_num, ])
    elif recommend_type == 2:
        list_data_set = blog_model.Blog.objects.raw(
            "select count(1) as count, user_app_userinfo.id, user_app_userinfo.username,"
            " user_app_userinfo.user_nick, user_app_userinfo.user_info, user_app_userinfo.avatar"
            " from blog_app_blog LEFT JOIN user_app_userinfo on  blog_app_blog.publisher_id = user_app_userinfo.id"
            " GROUP BY blog_app_blog.publisher_id ORDER BY count DESC LIMIT %s", params=[recommend_num, ])
    else:
        return ResultDict.get_error_response("排序方式有误")
    print(sql_result_util.result_to_list(list_data_set))
    return ResultDict.get_success_response(sql_result_util.result_to_list(list_data_set))


def index(request):
    return redirect(reverse('bbs_home'))


# 错误页面函数
def page_not_found(request, exception):
    return render(request, "error.html")
