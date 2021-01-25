from django.contrib import admin
from blog_app import models
# Register your models here.
admin.site.register(models.Blog)
admin.site.register(models.Types)
admin.site.register(models.Label)
admin.site.register(models.Comment)
admin.site.register(models.Favorite)
admin.site.register(models.Praise)