from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect

from utils.result_dict_util import ResultDict
from blog_app import models as blog_model


def home(request):
    blog_recommend_contents = []
    blog_recommend_contents = blog_model.Blog.objects.all()
    # 将数据按照规定每页显示5条, 进行分割
    pagibator = Paginator(blog_recommend_contents, 5)
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            blog_contents = pagibator.page(page)
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            blog_contents = pagibator.page(1)
        except InvalidPage:
            # 如果请求的页面不存在
            return HttpResponse("找不到页面内容")
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            blog_contents = pagibator.page(pagibator.num_pages)
    num_pages = pagibator.num_pages
    page = 1 if page is None else int(page)
    print('page:',page)
    print('num_pages:', num_pages)
    blog_contents = {"blog_contents": blog_contents, "current_num": page, "num_pages": num_pages}
    return render(request, "index.html", blog_contents)


def index(request):
    return redirect('/home/')
