from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'posts'

urlpatterns = [
    path('new/', login_required(views.New.as_view()), name='new'),
    path('', login_required(views.Index.as_view()), name='index'),
    path('<postId>/like/', login_required(views.Likes.as_view()), name='like'),
    path('<postId>/comment/', login_required(views.AddComment.as_view()), name='comment'),
    path('update/<int:pk>', login_required(views.UpdatePost.as_view()), name='update_post'),
    path('delete/<int:pk>', login_required(views.DeletePost.as_view()), name='delete_post'),
]