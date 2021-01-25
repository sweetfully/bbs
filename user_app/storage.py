'''
重写 models.FileField 上传文件时在数据库中保存的路径
'''
from django.core.files.storage import FileSystemStorage
from bbs.settings import MEDIA_URL


class AvatarStorage(FileSystemStorage):
    def _save(self, name, content):
        name = super(AvatarStorage, self)._save(name, content)
        print('='*20, name)
        return MEDIA_URL + name
