# from django.db import models
# from user_app.models import UserInfo
#
# # Create your models here.
#
#
# class Blog(models.Model):
#     # id
#     # 标题
#     # 内容（引用文件）
#     # 一小段内容
#     # 创建日期
#     # 更新日期
#     # 点赞数
#     # 评论数
#     # 阅读量
#     # 分类id    ->    分类表
#     # auther    ->    user表
#     # 标签id <->    标签表
#     title = models.CharField(max_length=50)
#     content = models.CharField(max_length=200)
#     content_paragraph = models.CharField(max_length=100)
#     create_data = models.DateTimeField(auto_now_add=True)
#     update_data = models.DateTimeField(auto_now_add=True, auto_now=True)
#     praise = models.IntegerField()
#     comment = models.IntegerField()
#     read_num = models.IntegerField()
#     publisher = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
#     # type = models.ForeignKey(to=)
#     # tag = models.ManyToManyField()
#
#
# class Comment(models.Model):
#     # id
#     # auther    ->    user表
#     # 评论内容
#     # 评论时间
#     # 评论博客id    ->    博客表
#     # 评论回复id    ->    评论表
#     commenter = models.ForeignKey(to=UserInfo, on_delete=models.SET_NULL)
#     content = models.CharField(max_length=100)
#     create_time = models.DateTimeField(auto_now_add=True)
#     blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE)
#
#
