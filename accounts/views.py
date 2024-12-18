from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth import login

from .forms import SignUpForm
from .models import User


# サインアップ画面
class SignUpView(generic.CreateView):
    # 使うformクラス設定
    form_class = SignUpForm
    # 使うテンプレートファイル設定
    template_name = 'registration/signup.html'

    # 成功時にログイン処理を行ってAccountDetailViewに飛ぶ
    def get_success_url(self):
        form = self.get_form()
        # usernameから登録したユーザー情報を参照
        user = User.objects.get(username=form.data.get('username'))

        # ログイン処理を行う
        login(self.request, user)
        return reverse(
            'accounts:userDetail',
            kwargs={'username': user.username})


# アカウント詳細画面
class AccountDetailView(DetailView):
    model = User
    # urlのパスクエリを引数に取る
    slug_field = 'username'
    slug_url_kwarg = 'username'

    # テンプレートに渡すデータにログイン中ユーザーの情報も追加する
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['login_user'] = self.request.user
        return context


# アカウント編集画面
class UserEdit(UpdateView):
    model = User
    template_name = 'accounts/user_edit.html'
    fields = ['icon', 'profile']

    def get_object(self):
        # ログイン中のユーザーで検索することを明示する
        return self.request.user

    def get_success_url(self):
        form = self.get_form()
        return reverse(
            'accounts:userDetail',
            kwargs={'username': self.request.user.username})
