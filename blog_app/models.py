from django.db import models
from user_app.models import UserInfo


# Create your models here.


# 分类表
class Types(models.Model):
    # id
    # 分类名称
    # 用户 <->    user表
    # 创建时间
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=30)
    user = models.ManyToManyField(to=UserInfo)
    create_time = models.DateTimeField(auto_now_add=True)


# 标签表
class Label(models.Model):
    # id
    # 标签名称
    # 用户 <->    user表
    # 创建时间
    label_id = models.AutoField(primary_key=True)
    label_name = models.CharField(max_length=30)
    user = models.ManyToManyField(to=UserInfo)
    create_time = models.DateTimeField(auto_now_add=True)


# 博客表
class Blog(models.Model):
    # id
    # 标题
    # 内容（引用文件）
    # 一小段内容
    # 创建日期
    # 更新日期
    # 点赞数
    # 评论数
    # 阅读量
    # 分类id    ->    分类表
    # author    ->    user表
    # 标签id <->    标签表
    # 博客评分（阅读量 * 1 + 点赞数 * 2 + 踩 * (-2) + 评论数 * 5）
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=400)
    content_paragraph = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    praise_num = models.IntegerField()
    dislike_num = models.IntegerField()
    comment_num = models.IntegerField()
    read_num = models.IntegerField()
    publisher = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    type = models.ForeignKey(to=Types, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(to=Label)
    score = models.IntegerField(default=0)


# 评论表
class Comment(models.Model):
    # id
    # author    ->    user表
    # 评论内容
    # 评论时间
    # 评论博客id    ->    博客表
    # 评论回复id    ->    评论表
    commenter = models.ForeignKey(to=UserInfo, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE)
    reply = models.ForeignKey(to='Comment', on_delete=models.CASCADE, null=True)


# 点赞表
class Praise(models.Model):
    # id
    # author    ->    user表
    # 点赞还是踩
    # 点赞时间
    # 点赞博客id    ->    博客表
    author = models.ForeignKey(to=UserInfo, on_delete=True)
    praise_id = models.AutoField(primary_key=True)
    praise_bad_review = models.IntegerField()
    praise_time = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('author', 'blog')


# 收藏表
class Favorite(models.Model):
    # id
    # 收藏夹名称
    # author    ->    user表
    # 博客id    ->    博客表
    # 收藏时间
    name = models.CharField(max_length=50)
    author = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'blog')
