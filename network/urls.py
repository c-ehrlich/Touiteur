from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

import debug_toolbar

from . import views

urlpatterns = [
    # View Routes
    path("", views.index, name="index"),
    path("account", views.account, name="account"),
    path("dms", views.dms, name="dms"),
    path("dm_thread/<str:username>", views.dm_thread, name="dm_thread"),
    path("following", views.following, name="following"),
    path("likes/<str:username>", views.likes, name="likes"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("mentions", views.mentions, name="mentions"),
    path("post/<int:id>", views.post, name="post"),
    path("register", views.register, name="register"),
    path("register2", views.register2, name="register2"),
    path("register3", views.register3, name="register3"),
    path("user/<str:username>", views.user, name="user"),

    # API Routes
    path("clear_mentions_count", views.clear_mentions_count, name="clear_mentions_count"),
    path("compose", views.compose, name="compose"),
    path("get_notifications", views.get_notifications, name="get_notifications"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("like/<int:post_id>", views.like, name="like"),
    path("new_posts", views.new_posts, name="new_posts"),
    path("reply/<int:post_id>", views.reply, name="reply"),
    path("thread_read_status/<int:thread_id>", views.thread_read_status, name="thread_read_status"),

    # Debug Routes
    path('__debug__/', include(debug_toolbar.urls)),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# TODO in deployment serve files in the proper way
# see: https://docs.djangoproject.com/en/3.2/howto/static-files/deployment/
