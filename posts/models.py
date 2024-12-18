from django.db import models
from accounts.models import User
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFit
from taggit.managers import TaggableManager


class Post(models.Model):
    # 外部キーとしてaccounts.Userと紐付けするためのカラム
    author = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE)
    # 画像を登録するためのカラム
    # 16:9の割合でリサイズするようにしている
    picture = ProcessedImageField(upload_to='image/posts', blank=False, null=False,
                        processors=[ResizeToFit(1024, 576)],
                        format='JPEG', options={'quality': 100})
    # 写真のコメントを追加するためのカラム
    text = models.TextField(blank=True)
    # タグを持つためのカラム
    tags = TaggableManager(blank=True)
    # 投稿日を持つためのカラム
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class Like(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    text = models.TextField(blank=True)
