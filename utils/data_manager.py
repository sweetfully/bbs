import random
import os
import requests
from fake_useragent import UserAgent
from lxml import etree

blog_types = ("教学", "信息", "测评", "清单", "采访", "案例分析", "人物专访", "链接汇总", "问题", "对比", "激情", "励志", "研究", "整理",
              "预测和总结", "批判", "辩论", "假想",
              "讽刺", "活动",)


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
            app_models.UserInfo.objects.create_user(username="ID%d" % (300000 + i), password="1234abcd",
                                                    user_nick=random.choice(nick_list),
                                                    avatar="/avatars/avatars/avatar%d.jpeg" % (random.randint(0, 29)),
                                                    phone="133456%d" % (10000 + i * 9),
                                                    email="%d@qq.com" % (10000 + i * 135))


# 创建 num 个用户的关注关系
def create_user_concern(num):
    all_user_list = app_models.UserInfo.objects.all()
    for i in range(num):
        app_models.Focus.objects.create(focus_people=random.choice(all_user_list),
                                        be_focus_people=random.choice(all_user_list))


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


# 爬取网上博客并保存
def create_blog():    # 可以创建38条数据
    blog_url_list = ["https://www.cnblogs.com/pick/", "https://www.cnblogs.com/candidate/"]
    all_user_list = app_models.UserInfo.objects.all()
    for blog_url in blog_url_list:
        resp = requests.get(blog_url, headers={"User-Agent": UserAgent().chrome})
        if resp.status_code == 200:
            resp.encoding = "utf-8"
            doc = etree.HTML(resp.text)
            blog_title_list = doc.xpath('//a[@class="post-item-title"]/text()')
            blog_content_list = doc.xpath('//p[@class="post-item-summary"]')
            for i in range(len(blog_title_list)):
                blog_content = blog_content_list[i].xpath("string(.)").strip()
                user = random.choice(all_user_list)
                all_type_list = blog_models.Types.objects.filter(user=user)
                all_label_list = blog_models.Label.objects.filter(user=user)
                try:
                    blog_obj = blog_models.Blog.objects.create(title=blog_title_list[i],
                                                               content=blog_content,
                                                               content_paragraph=blog_content,
                                                               praise_num=0,
                                                               comment_num=0,
                                                               dislike_num=0,
                                                               read_num=random.randint(0, 500),
                                                               publisher=user,
                                                               type=random.choice(all_type_list), )
                    blog_obj.tag.set(random.choices(all_label_list, k=3))
                except:
                    print("字符编码有问题，标题：%s, 内容：%s"%(blog_title_list[i], blog_content))


# 创建 num 个评论
def create_blog_comment(num):
    # all_blog_list = blog_models.Blog.objects.all()
    pass


# 创建 num 个赞或者踩
def create_blog_praise(num):
    all_blog_list = blog_models.Blog.objects.all()
    all_user_list = app_models.UserInfo.objects.all()
    for i in range(num):
        try:
            blog_obj = random.choice(all_blog_list)
            user_obj = random.choice(all_user_list)
            is_like = random.randint(0, 100)//80
            blog_models.Praise.objects.create(blog=blog_obj, author=user_obj, praise_bad_review=is_like)
            if is_like == 1:
                blog_obj.praise_num = blog_obj.praise_num + 1
            else:
                blog_obj.dislike_num = blog_obj.dislike_num + 1
            blog_obj.save()
        except:
            print("某用户对某博客重复点赞了")


# 创建 num 个收藏
def create_blog_favorite(num):
    all_blog_list = blog_models.Blog.objects.all()
    all_user_list = app_models.UserInfo.objects.all()
    for i in range(num):
        try:
            blog_obj = random.choice(all_blog_list)
            user_obj = random.choice(all_user_list)
            blog_models.Favorite.objects.create(blog=blog_obj, author=user_obj)
        except:
            print("某用户对某博客重复收藏了")
        pass


def create_user_detail_info():
    all_user_list = app_models.UserInfo.objects.all()
    for user in all_user_list:
        user_detail_info = app_models.UserDetailInfo.objects.create(age=random.randint(10, 50),
                                                                    sex=random.randint(0, 1),
                                                                    hometown="山东省青岛市")
        user.detail_info = user_detail_info
        user.save()


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bbs.settings')  # 这句话在manage.py中可以复制
    import django

    django.setup()
    from user_app import models as app_models
    from blog_app import models as blog_models
    # create_user(100)
    # create_user_concern(200)
    # create_blog_type()
    # create_blog_tag(100)
    # create_blog()
    # create_blog_comment(100)
    # create_blog_praise(300)
    # create_blog_favorite(250)
    # create_user_detail_info()

