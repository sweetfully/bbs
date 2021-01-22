from django.db import models
from user_app.models import UserInfo

# Create your models here.


#分类表
class Types(models.Model):
    # id
    # 分类名称
    # 用户 <->    user表
    # 创建时间
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=20)
    username = models.ManyToManyField(to=UserInfo)
    create_time = models.DateTimeField(auto_now_add=True)

#标签表
class Label(models.Model):
    # id
    # 标签名称
    # 用户 <->    user表
    # 创建时间
    label_id = models.AutoField(primary_key=True)
    label_name = models.CharField(max_length=100)
    username = models.ManyToManyField(to=UserInfo)
    create_time = models.DateTimeField(auto_now_add=True)


#博客表
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
    # auther    ->    user表
    # 标签id <->    标签表
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    content_paragraph = models.CharField(max_length=100)
    create_data = models.DateTimeField(auto_now_add=True)
    update_data = models.DateTimeField(auto_now_add=True, auto_now=True)
    praise = models.IntegerField()
    comment = models.IntegerField()
    read_num = models.IntegerField()
    publisher = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    type_id = models.ForeignKey(to=Types)
    tag_id = models.ManyToManyField(to=Label)

#评论表
class Comment(models.Model):
    # id
    # auther    ->    user表
    # 评论内容
    # 评论时间
    # 评论博客id    ->    博客表
    # 评论回复id    ->    评论表
    commenter = models.ForeignKey(to=UserInfo, on_delete=models.SET_NULL)
    content = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(to=Blog, to_field= '', on_delete=models.CASCADE)
    comments_blog_id = models.ForeignKey(to=Blog, on_delete=models.CASCADE)
    comments_reply_id = models.ForeignKey(to=Blog, on_delete=models.CASCADE)

#点赞表
class Praise(models.Model):
    # id
    # auther    ->    user表
    # 点赞还是踩
    # 点赞时间
    # 点赞博客id    ->    博客表
    praise_id = models.AutoField(primary_key=True)
    auther = models.ForeignKey(to=UserInfo,on_delete=True)
    praise_Bad_review = models.IntegerField()
    praise_time = models.DateTimeField(auto_now_add=True)
    praise_blog_id = models.ForeignKey(to=Blog, on_delete=models.CASCADE)

#关注表
class Focus(models.Model):
    # id
    # 关注人    ->    user表
    # 被关注人    ->    user表
    #
    focus_id = models.AutoField(primary_key=True)
    focus_people = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    be_focus_people = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)

#收藏表
class Collection(models.Model):
    # id
    # auther    ->    user表
    # 博客id    ->    博客表
    # 收藏时间
    collection = models.AutoField(primary_key=True)
    auther = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    blog_id = models.ForeignKey(to=Blog, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)


