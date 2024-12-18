from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFit



# AbstractUser: Djangoが用意しているUserモデルを継承する
class User(AbstractUser):
    # アイコンをリサイズした画像だけ保存するProcessedImageFieldとして定義する
    icon = ProcessedImageField(upload_to='image/icons', blank=True, null=True,
                               default='image/icons/kyokusyou_symbol_bo9rwy.jpg',
                               processors=[ResizeToFit(400, 400)],
                               format='JPEG',
                               options={'quality': 100})
    profile = models.TextField(verbose_name="プロフィール",
                               max_length=200, blank=True, null=True)

    # icon画像が登録されずにユーザー情報が更新された時のValueErrorを防ぐ
    @property
    def icon_url(self):
        if self.icon and hasattr(self.icon, 'url'):
            return self.icon.url
        return None

    # 作成を成功したら'accounts:Detail'と定義されているURLに飛ぶ
    def get_absolute_url(self):
        return reverse(
            'accounts:userDetail', kwargs={'username': self.username})

