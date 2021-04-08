from django.shortcuts import render
from django.db.models import Count, Sum
from django.contrib.auth.decorators import login_required
from user_app import models as user_models
from blog_app import models as blog_models
from utils import sql_result_util
from utils.result_dict_util import ResultDict

BLOG_NUM_BY_PAGE = 4
BLOG_SORT_DICT = {1: "-create_date", 2: "-praise_num", 3: "-read_num",
                  -1: "create_date", -2: "praise_num", -3: "read_num"}


def get_blog_home(request, username):
    print("username：", username)
    user_set = user_models.UserInfo.objects.filter(username=username).values("id", "username", "email", "date_joined",
                                                                             "user_nick", "phone", "avatar", "user_info")
    print(len(user_set))
    if len(user_set):
        # blog_set = blog_models.Blog.objects.filter(publisher__username=username)
        # print(len(blog_set), blog_set)
        response_content = {"user": user_set[0]}
        if request.user.is_authenticated:
            # 若用户登录了
            if request.user.username == username:
                # 如果个人博客是自己的博客的话则右上角按钮文本设置为“个人中心”
                response_content.setdefault("btn_type", 0)
            else:
                # 如果不是自己，那么就判断是否有关注对方
                focus_set = user_models.Focus.objects.filter(focus_people__username=request.user.username,
                                                             be_focus_people__username=username)
                if len(focus_set) == 0:
                    # 若没有有关注，右上角按钮文本设置为“关注”
                    response_content.setdefault("btn_type", 1)
                else:
                    # 若有关注，右上角按钮文本设置为“取消关注”
                    response_content.setdefault("btn_type", 2)
        else:
            # 若用户未登录，那么右上角按钮文本设置为“关注”，点击的时候跳转到登录窗口即可
            response_content.setdefault("btn_type", 1)
        # 更新博客数和阅读数, 因为需要使用MySQL的IFNULL函数，所以直接写SQL语句
        blog_set = blog_models.Blog.objects.raw(
            "SELECT user_app_userinfo.id, COUNT(1) AS blog_count, " +
            "IFNULL(SUM(blog_app_blog.read_num), 0) AS read_mun_sum " +
            "FROM blog_app_blog INNER JOIN user_app_userinfo " +
            "ON (blog_app_blog.publisher_id = user_app_userinfo.id) " +
            "WHERE user_app_userinfo.username = %s", params=[username, ])
        response_content.update(sql_result_util.result_to_list(blog_set)[0])

        # 更新粉丝数
        fans_set = user_models.Focus.objects.filter(be_focus_people__username=username).aggregate(fans_count=Count("*"))
        response_content.update(fans_set)

        # 通过统计所有博客的分数来得到用户的排名(由于使用了left join，因此使用原生的sql写代码（默认是inner join）)
        user_rank_set = user_models.UserInfo.objects.raw(
            "SELECT * FROM (SELECT @rownum:=@rownum+1 as rank,t.* " +
            "FROM (SELECT @rownum:=0) a, " +
            "(SELECT user_app_userinfo.id, user_app_userinfo.username, SUM(blog_app_blog.score) AS score_sum " +
            "FROM user_app_userinfo left JOIN blog_app_blog " +
            "ON (blog_app_blog.publisher_id = user_app_userinfo.id) " +
            "GROUP BY user_app_userinfo.username " +
            "ORDER BY score_sum DESC, user_app_userinfo.date_joined) t) a " +
            "where a.username = %s", params=[username, ])
        response_content.setdefault("user_rank", int(getattr(user_rank_set[0], "rank")))

        print(response_content)
        return render(request, "blog_home.html", response_content)
    return render(request, "error.html")


def get_blog_list_by_username(request):
    user_id = getattr(request, request.method).get('userId')
    page = int(getattr(request, request.method).get('page', 1))
    sort = int(getattr(request, request.method).get('sort', 1))
    print(user_id, page, sort)
    if not user_id:
        return ResultDict.get_error_response("username不可为空")
    user = user_models.UserInfo.objects.get(id=user_id)
    if not user:
        return ResultDict.get_error_response("此用户ID不正确!")
    start_position = (page - 1) * BLOG_NUM_BY_PAGE
    end_position = page * BLOG_NUM_BY_PAGE
    blog_list = blog_models.Blog.objects.filter(publisher=user) \
        .order_by(BLOG_SORT_DICT[sort])[start_position: end_position]
    print(blog_list)
    return ResultDict.get_success_response(sql_result_util.list_to_dict(blog_list))


def get_favorite_dir(request):
    user_id = getattr(request, request.method).get('userId')
    page = int(getattr(request, request.method).get('page', 1))
    if not user_id:
        return ResultDict.get_error_response("username不可为空")
    user = user_models.UserInfo.objects.get(id=user_id)
    if not user:
        return ResultDict.get_error_response("此用户ID不正确!")
    new_time = blog_models.Favorite.objects.filter(author=user).order_by("-create_time").values("create_time").first()
    blog_count = blog_models.Favorite.objects.filter(author=user).aggregate(blog_count=Count(1))
    favorite_dict = {"id": -1, "favorite_name": "默认收藏夹"}
    if not new_time:
        favorite_dict.update(new_time)
    if not blog_count:
        favorite_dict.update(blog_count)
    return ResultDict.get_success_response([favorite_dict, ])


def get_favorite_list(request):
    user_id = getattr(request, request.method).get('userId')
    favorite_dir_id = int(getattr(request, request.method).get('favoriteDirId', -1))  # 收藏夹ID, 暂时没有用
    page = int(getattr(request, request.method).get('page', 1))
    print(user_id, favorite_dir_id, page)
    if not user_id:
        return ResultDict.get_error_response("username不可为空")
    user = user_models.UserInfo.objects.get(id=user_id)
    if not user:
        return ResultDict.get_error_response("此用户ID不正确!")
    start_position = (page - 1) * BLOG_NUM_BY_PAGE
    end_position = page * BLOG_NUM_BY_PAGE
    favorite_list = blog_models.Favorite.objects.filter(author=user) \
                             .order_by("-create_time")[start_position: end_position]
    return ResultDict.get_success_response(sql_result_util.list_to_dict([favorite.blog for favorite in favorite_list],
                                                                        foreign_key_field="publisher",
                                                                        foreign_key_field_rename="user",
                                                                        pop_foreign_key_fields=["password"]))


def message_manager_list(request):
    return render(request, "message_manager.html")


@login_required
def write_blog(request):
    if request.method == "POST":
        return ResultDict.get_success_response()
    return render(request, "write_blog.html")
