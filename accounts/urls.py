from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),  # ユーザー追加画面
    path('<username>/', login_required(views.AccountDetailView.as_view()), name='userDetail'),  # ユーザー詳細画面
    path('user/edit/', login_required(views.UserEdit.as_view()), name='user_edit'),  # アイコン編集画面
]
