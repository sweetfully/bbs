from math import ceil

from django.shortcuts import render, redirect
from blog_app import models as blog_model
from utils.result_dict_util import ResultDict


def home(request):
    # 得到请求链接中page的值，如果没值设置默认值1
    page = int(getattr(request, request.method).get('page', 1))
    # 计算当前页的第一条记录
    start_num = (page - 1) * 4
    # 计算当前页的最后一条记录
    end_num = page * 4
    # limit限制取数
    blog_contents = blog_model.Blog.objects.all()[start_num:end_num]
    # 总页数（向上取整）
    num_pages = ceil(blog_model.Blog.objects.count() / 4)
    # 如果没有数据，不显示分页组件和列表
    if num_pages == 0:
        return render(request, "index.html", "没有数据")
    else:
        blog_contents = {"blog_contents": blog_contents, "current_num": page, "num_pages": num_pages}
        return render(request, "index.html", blog_contents)


def phb_list(request):
    list_data = list(blog_model.Blog.objects.order_by("-praise_num")[0:4])
    print("list_data:", list_data[0].praise_num)
    return ResultDict.get_success_response(list_data)


def index(request):
    return redirect('/home/')


# 错误页面函数
def page_not_found(request, exception):
    return render(request, "error.html")
