## Djangoプロジェクト全体について


### 仮想環境の構築
PyCharm でPythonのバージョンごとにプロジェクトを作って管理しているが
Python36のフォルダで間違ってpipenv installしてpipenv —rmして削除したが
残ったPipfileに”python = 3.8”との記述があった。なんで？
その後Python36フォルダのPreferencesを確認したらPython Interpreterが3.6に設定されて無かったのが原因か？とりあえずPython Interpreterを3.6に設定しといたが。

https://www.techpit.jp/courses/554782/lectures/10061281
を参考に
```terminal:
$ python -m django startproject techpitgram
```
を実行しても
djangoがないって言われる…Python36フォルダにはPipfileがないからdjango
インストールされないってこと？

Python36フォルダを開いたら
仮想環境の名前が(venv)になっていたのでstudysnsディレクトリに入って
pipenv shellを実行
Djangoを入れるために
pipenv　lockしてpipenv updateしようとしたらpipenv lockにやたら時間かかっている

ここまでやって
https://akiyoko.hatenablog.jp/entry/2018/06/17/182651
の通りにすればよかったことに気づいたやんけ

もしpipenv　--rmでPyCharmが作った仮想環境が削除できなかった時は
https://stackoverflow.com/questions/57100248/how-to-remove-a-virtualenv-which-is-created-by-pycharm


### StudySNSの制作
1.モジュールのインポートエラー
```djangotemplate
from django.urls import reverse
         ^
SyntaxError: invalid character in identifier
```
と出たが該当行を一旦削除して記述し直したらエラーが出なくなった


2.モジュールのインポートエラー２
```djangotemplate
from accounts.models import User
```
ここがUnresolved reference 'accounts' を吐いていたので..accounts.modelsと修正したら
逆にmakemigrationsが通らなくなった
解決策は1.と同じかな？

3.変数のエラー
```djangotemplate
ValueError: attempted relative import beyond top-level package
```

```djangotemplate
File "/Users/danna/.local/share/virtualenvs/Django22-sb5Nc4g4/lib/python3.6/site-packages/django/db/models/fields/files.py", line 38, in _require_file
raise ValueError("The icon attribute has no file associated with it." icon self.field.name)
```

accounts/admin.pyに
```djangotemplate
accounts/admin.py
admin.site.register(User)
```
を追加してアイコンをDjangoのadmin管理機能から登録したら直った


4.カスタムフィルター
カスタムフィルターを追加したらテンプレートのHTMLの頭に
{% load custom_filter %}をつけるのを忘れないこと


5.インデントエラー
```djangotemplate
django.template.exceptions.TemplateSyntaxError: Invalid filter: 'get_comment_list'
```
どうやら@register.filter():のインデントがまずかったようだ


6.サーバーのジョブの終了のさせ方
ctrl+zでサーバーストップさせたらkillコマンドしてもjobが終了されない
exitやlogoutコマンドを実行すると以下のメッセージ
```djangotemplate
[1]  + suspended  python manage.py runserver
```
susupendedしてるものは
```kill %1```とjobの番号この場合[1]を指定して殺す


7.画像の保存先をcloudinaryに設定
CloudinaryのCLOUD_NAMEやAPI_KEYをHerokuに設定しローカルでも動くようにする
KeyError: 'CLOUDINARY_CLOUD_NAME'


8. Herokuにデプロイするための設定
https://qiita.com/frosty/items/66f5dff8fc723387108c
を参考に進める
psycopg2がインストールされない
先にデータベースをPostgreDBに置き換えてから必要なモジュールをインストールすべきか
PyCharmで以下のようなメッセージが出たが何か
Plugins supporting Pipfile files found

途中
```Heroku
remote:  !     No default language could be detected for this app.
remote:                         HINT: This occurs when Heroku cannot detect the buildpack to use for this application automatically.
```
ビルドパックを設定していないことによるエラ〜らしいので
```$ heroku buildpacks:set heroku/python```
を実行しても
```Heroku
remote: -----> App not compatible with buildpack: https://buildpack-registry.s3.amazonaws.com/buildpacks/heroku/python.tgz
remote:        More info: https://devcenter.heroku.com/articles/buildpacks#detection-failure
```
https://yoshitaku-jp.hatenablog.com/entry/2018/11/13/151505
上記によるとrequirements.txtがないことによるものらしいPipfileだけじゃダメ
```zsh
% pip freeze > requirements.txt
```
を実行する
requirements.txtを見るとpsycopg2がインストールされてない
もう一回
```zsh
pipenv install
```
またエラ〜
```Heroku
Error: pg_config executable not found.', '    
', '    pg_config is required to build psycopg2 from source.  Please add the directory', '
```
runtime.txtを作成してなかった
```zsh
$ echo python-3.7.3 > runtime.txt
```
Django Girls Tutorialを見ると
https://tutorial-extensions.djangogirls.org/ja/heroku/
requirements.txtファイルを開いて、次の行を一番下に追加しましょう：
```zsh:requirements.txt
psycopg2==2.7.6.1
```
なんてこったい！
```djangotemplate:settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycpopg2',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': '',
        'HOST': 'host',
        'PORT': '',
    }
}
```
タイポミスじゃないかーーーwwwwwwwww
誤：psycpopg2
正：psycopg2

Pipfileに
```zsh:Pipfile
psycopg2==2.7.6.1
```
を追加して
```zsh
% pipenv install
% pip freeze > requirements.txt
```
を実行してrequirement.txtにpsycopg2を設定してみる


10. Userモデルのiconの画像をimagekitでリサイズしてcloudinaryに保存されるようにする

makemigrationsをかけると
```zsh
ModuleNotFoundError: No module named 'stdimage'
```
stdimageモジュールでリサイズしようとしていた時のmigrationファイルが残ってしまっていた

```zsh
% git reset --hard HEAD
```
をしてstdimageの記述が残っているaccounts/migrations/0002_auto_20200618_1134.pyを消そうとしても消えなかった
原因は上記のファイルがステージングされてなかったのでそもそもgitでは消せなかったこと


11.管理者権限のユーザーがいなくなってしまったのでDjangoのシェルから管理者権限を付与する
```djangotemplate
>>> python manage.py shell
>>> from accounts.models import User
>>> users = User.objects.all()
>>> user = users[0]
>>> user
<User: yamada>
>>> user.is_superuser = True
```
管理権限が付与されない…なんでだ
```zsh
% python manage.py createsuperuser
```
これで解決


12.アイコン編集ボタンがユーザー詳細画面に出ない
accounts/view.pyで
```djangotemplate
context['login_user'] = self.request.user
```
とすべきところを
```zsh
context['login_user'] = 'self.request.user'
```
と囲ってしまっていた


13.Heorkuにプッシュ
```zsh
 ! [remote rejected] master -> master (pre-receive hook declined)
```
モジュールを新しく入れたのにrequirements.txtが更新されていなかったせい
新しいモジュールをPipfileに追加した時は必ず以下を行う
```zsh
% pipenv install
% pip freeze > requirements.txt
% heroku run python manage.py migrate
```

```Heroku:Build log
Post-processing 'admin/css/forms.css' failed!
whitenoise.storage.MissingFileError: The file 'admin/css/widgets.css' could not be found with
<whitenoise.storage.CompressedManifestStaticFilesStorage object at 0x7f9aa03b6c18>
中略
Please check the URL references in this CSS file, particularly any
       relative paths which might be pointing to the wrong location.
```
どうやらstaticfilesの設定がまずいらしいのでsettings.pyにあるSTATIC_ROOTの設定を削除する

ダメだったので以下に修正
```django:settings.py
INSTALLED_APPS = [ 'django.contrib.static',]
```
ダメだったのでorigin/masterのsettings.pyを見てみると
MEDIA_ROOTがコメントアウトされているので同様に修正

ダメだったのでstaticディレクトリをstaticfilesに修正


14.投稿一覧のアイコン画像を小さく表示する

機能要件
(1)アイコン画像を登録しなくても初期値のアイコン画像を登録してくれる
(2)アイコン画像のオリジナルはcloudinaryに保存させない
(3)投稿一覧画面に表示する投稿者のアイコンは50x50の小さいサイズ

試した方法
①ImageKitはリサイズしたオリジナル画像だけ保存してくれるProcessedImageFieldと
オリジナル画像からCACHEに仮想的に画像を生成してくれるImageSpecFieldがあるが
ImageSpecFieldで生成された画像をCloudinaryに保存するとurlに余計なサフィックスがついてしまい
テンプレートでauther.user.icon_thumbnail.urlを指定しても取得できない
②リサイズされたオリジナルの画像とサムネイルを同時に生成してUserモデルにアイコン画像のフィールドを一つだけにしたいなら
django-stdimageがあるがオリジナルのリサイズされていない画像も保存されてしまう
それにやはりテンプレートでサムネイルのurlを取得できない
③これまで通りBootstrapで小さくレスポンシブで表示できれば良いが…なぜかレスポンシブにならない
④解決した方法
```djangotemplate:templates/index.html
{% load cloudinary %}
{% cloudinary post.author.icon.url width=50 height=50 %}
```
Cloudinary様様でした。1日半かかった…長かった


15.ImageField(ProcessedImageField)にblank/null=Trueを設定していても変数エラーが起こる
```djnagotemplate
ValueError: The 'icon' attribute has no file associated with it.
```
https://code.djangoproject.com/ticket/13327
によると同じようなエラーに悩まされていて
The model propertyを追加すれば良いらしい
それが以下のデコレーター関数みたいなものだが

```djangotemplate
@property
def image_url(self):
    if self.image and hasattr(self.image, 'url'):
        return self.image.url
```
これは@property以下の関数をfunc()のように書かなくても返り値をモデルのプロパティのように扱って
くれるものらしい。モデルに姓と名別々のフィールドがあったとして関数でその2つのフィールドをつなげて
フルネームをモデルのプロパティのように扱えるようにしたい時など。
https://stackoverflow.com/questions/58558989/what-does-djangos-property-do
```djangotemplate:accoutns/models.py
    # icon画像が登録されずにユーザー情報が更新された時のValueErrorを防ぐ
    @property
    def icon_url(self):
        if self.icon and hasattr(self.icon, 'url'):
            return self.icon.url
        return cloudinary.utils.cloudinary_url("media/image/icons/kyokusyou_symbol_bo9rwy.jpg")[0]
```


### 本番環境にビルド（さくらVPS)
https://qiita.com/clutter/items/5e319bdf707e4e76d463
ここを参考にOSイントールから構築していく

1. ssh登録
```commandline
% scp id_rsa.pub danna@ホスト名/
```
これだとPermission denied
```commandline
% scp id_rsa.pub danna@アドレス/
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ECDSA key sent by the remote host is
SHA256:XZ+xVVB2prGyMWJR+5exmUvrInlAjkUgIpZlWc5muWk.
Please contact your system administrator.
```
IPv4アドレスで送るとこんな警告が出る
さらにβ版のシリアルコンソールでないと公開鍵をコピペできない

rootにetcなどフォルダが全くないんですけど…
```commandline
[root@ik1-413-38762 ~]# cd ..
[root@ik1-413-38762 /]# ls
bin   dev  home  lib64       media  opt   root  sbin  sys  usr
boot  etc  lib   lost+found  mnt    proc  run   srv   tmp  var
```
どうやら特定のユーザーで入ると初期状態でroot "/" にはいないらしいが
このチルダ"~"と"/"の違いはなに？
~/home/user/となっているってことは特定のユーザーのディレクトリってころかな

.ssh/configmp設定でホスト名に''はつけなくて良かった…ハマった
いやどうやってもPermission Deniedでポートも50022をしていしているのにそれ以外のポートでアクセスしようとする

```commandline
%su danna
%su - danna # 環境変数を引き継がずにユーザー変更
```

```commandline
debug1: Authentications that can continue: publickey,gssapi-keyex,gssapi-with-mic
debug2: we did not send a packet, disable method
debug1: No more authentication methods to try.
danna@ik1-413-38762.vs.sakura.ne.jp: Permission denied (publickey,gssapi-keyex,gssapi-with-mic).

```
なんでたかがsshでログインするだけで5時間もかけねーといけねーんだよ○ね

https://qiita.com/You_name_is_YU/items/c0f71f4d5dcf49dc7f89
上記の通りカスタムインストールで解決

上記に追加して行ったこと
```commandline
% chmod 600 .ssh/authorized_keys
```
そして以下も設定
https://www.rem-system.com/centos8-first-settings/


2. Djangoのインストール
サーバーにプロジェクト用ディレクトリ作成
```commandline
$ mkdir /var/www
```
以前/user/project_nameにftpでローカルのソース持ってきてpip install -r requiremants.txt
してあったが、プロジェクトを作ろうとすると
```commandline
$ sudo django-admin startproject studysns
```
sudo: django-admin: コマンドが見つかりません
となってしまうのでpathを通してみる
```commandline
$ sudo python /usr/local/lib/python3.6/site-packages/django/bin/django-admin.py startproject my-project
```
これでできた

3. Djangoの開発用サーバーで使用するポート8000を解放
さくらVPSのパケットフィルタとCentOSのファイヤウォールの２つを開放して上げなくてはいけない。
```commandline
$ sudo firewall-cmd --add-port=8000/tcp --zone=public --permanent
$ sudo firewall-cmd --reload
```
上記のようにリロードしないと開放されないので注意

4.