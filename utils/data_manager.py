import random
import os
import requests
from fake_useragent import UserAgent
from lxml import etree
import json

blog_types = ("教学", "信息", "测评", "清单", "采访", "案例分析", "人物专访", "链接汇总", "问题", "对比", "激情", "励志",
              "研究", "整理", "预测和总结", "批判", "辩论", "假想", "讽刺", "活动",)


# 创建 num 个用户
def create_user(num):
    resp = requests.get("http://www.duanmeiwen.com/mingzi/47160.html", headers={"User-Agent": UserAgent().chrome})
    if resp.status_code == 200:
        resp.encoding = "gb2312"
        doc = etree.HTML(resp.text)
        result_list = doc.xpath('//div[@class="content"]/p/text()')
        nick_list = []
        for nick in result_list:
            if "、" in nick:
                nick_list.append(nick.split("、")[1])
        print(nick_list)
        for i in range(num):
            user_detail_info = app_models.UserDetailInfo.objects.create()
            app_models.UserInfo.objects.create_user(username="ID%d" % (300000 + i), password="1234abcd",
                                                    user_nick=random.choice(nick_list),
                                                    avatar="/avatars/avatars/avatar%d.jpeg" % (random.randint(0, 29)),
                                                    phone="133456%d" % (10000 + i * 9),
                                                    email="%d@qq.com" % (10000 + i * 135),
                                                    user_info="这个人很懒，什么都没留下",
                                                    detail_info=user_detail_info)


# 创建 num 个用户的关注关系
def create_user_concern(num):
    all_user_list = app_models.UserInfo.objects.all()
    index = 0
    for i in range(num):
        try:
            app_models.Focus.objects.create(focus_people=random.choice(all_user_list),
                                            be_focus_people=random.choice(all_user_list))
        except Exception:
            print("这个人已经被关注了，next。")
            index += 1
    print("有%s组关系重复了"%index)


# 创建博客类型
def create_blog_type():
    all_user_list = app_models.UserInfo.objects.all()
    for blog_type in blog_types:
        type_obj = blog_models.Types.objects.create(type_name=blog_type)
        type_obj.user.set(random.choices(all_user_list, k=random.randint(0, len(all_user_list))))


# 创建 num 个用户的博客标签
def create_blog_tag(num):
    all_user_list = app_models.UserInfo.objects.all()
    for i in range(num):
        label_obj = blog_models.Label.objects.create(label_name="标签%d" % i)
        label_obj.user.set(random.choices(all_user_list, k=random.randint(0, len(all_user_list) // 2)))


def get_csdn_url():
    url_types = ["home", "db", "java", "python", "web", "arch", "mobile", "sec"]
    url = "https://blog.csdn.net/api/articles?type=more&category={}&shown_offset={}"
    for url_type in url_types:
        for i in range(15):
            yield url.format(url_type, i)


# 爬取网上num篇博客并保存
def create_blog(num):    # 可以创建38条数据
    all_user_list = app_models.UserInfo.objects.all()
    index = 0
    for blog_url in get_csdn_url():
        resp = requests.get(blog_url, headers={"User-Agent": UserAgent().chrome})
        if resp.status_code == 200:
            resp_dict = json.loads(resp.text)
            for article in resp_dict["articles"]:
                blog_title = article["title"]
                blog_content = article["desc"]
                user = random.choice(all_user_list)
                all_type_list = blog_models.Types.objects.filter(user=user)
                all_label_list = blog_models.Label.objects.filter(user=user)
                try:
                    blog_obj = blog_models.Blog.objects.create(title=blog_title,
                                                               content=blog_content,
                                                               content_paragraph=blog_content,
                                                               url=1000000 + index * 3,
                                                               praise_num=0,
                                                               dislike_num=0,
                                                               comment_num=0,
                                                               read_num=random.randint(0, 500),
                                                               publisher=user,
                                                               type=random.choice(all_type_list),
                                                               score=0)
                    blog_obj.tag.set(random.choices(all_label_list, k=3))
                except:
                    print("字符编码有问题，标题：%s, 内容：%s" % (blog_title, blog_content))
                index += 1
                if index > num:
                    return


# 创建 num 个评论
def create_blog_comment(num):
    # all_blog_list = blog_models.Blog.objects.all()
    pass


# 创建 num 个赞或者踩
def create_blog_praise(num):
    all_blog_id_list = blog_models.Blog.objects.values("id")
    all_user_id_list = app_models.UserInfo.objects.values("id")
    index = 0
    for i in range(num):
        try:
            blog_id = random.choice(all_blog_id_list)["id"]
            user_id = random.choice(all_user_id_list)["id"]
            print(blog_id, user_id)
            is_like = 1 - random.randint(0, 100)//80
            with transaction.atomic():
                blog_models.Praise.objects.create(blog_id=blog_id, author_id=user_id, praise_bad_review=is_like)
                blog_obj = blog_models.Blog.objects.get(id=blog_id)
                print(blog_obj)
                if is_like == 1:
                    blog_obj.praise_num = blog_obj.praise_num + 1
                else:
                    blog_obj.dislike_num = blog_obj.dislike_num + 1
                blog_obj.save()
        except:
            print("某用户对某博客重复点赞了")
            index += 1
    print("共有%s个重复记录" % index)


# 创建 num 个收藏
def create_blog_favorite(num):
    all_blog_id_list = blog_models.Blog.objects.values("id")
    all_user_id_list = app_models.UserInfo.objects.values("id")
    index = 0
    for i in range(num):
        try:
            blog_id = random.choice(all_blog_id_list)["id"]
            user_id = random.choice(all_user_id_list)["id"]
            blog_models.Favorite.objects.create(blog_id=blog_id, author_id=user_id)
        except:
            print("某用户对某博客重复收藏了")
            index += 1
    print("共有%s个重复记录" % index)


def update_blog_score():
    result_num = blog_models.Blog.objects.update(
        score=F("read_num") * 1 + F("praise_num") * 2 + F("dislike_num") * (-2) + F("comment_num") * 5,
        url=1000000 + F("id") * 3)
    print("总共更新了%s条数据", result_num)


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bbs.settings')  # 这句话在manage.py中可以复制
    import django

    django.setup()
    from django.db import transaction
    from django.db.models import F
    from user_app import models as app_models
    from blog_app import models as blog_models
    # create_user(200)
    # create_user_concern(2000)
    # create_blog_type()
    # create_blog_tag(500)
    # create_blog(1000)
    # create_blog_comment(100)
    # create_blog_praise(6000)
    # create_blog_favorite(2000)
    # update_blog_score()


