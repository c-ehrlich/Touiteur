from django.conf import settings
# from django.conf.urls.i18n import i18n_patterns #only need this if we want to prepend url paths with language code
from django.conf.urls.static import static
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

import debug_toolbar

from . import views

urlpatterns = [
    # Needed for locale change
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += [
    # View Routes
    path("", views.index, name="index"),
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
    path("settings", views.settings, name="settings"),
    path("user/<str:username>", views.user, name="user"),

    # API Routes
    path("block_toggle/<int:user_id>", views.block_toggle, name="block_toggle"),
    path("block_toggle_username/<str:username>", views.block_toggle_username, name="block_toggle_username"),
    path("clear_mentions_count", views.clear_mentions_count, name="clear_mentions_count"),
    path("compose", views.compose, name="compose"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("like/<int:post_id>", views.like, name="like"),
    path("notifications", views.notifications, name="notifications"),
    path("reply/<int:post_id>", views.reply, name="reply"),
    path("thread_read_status/<int:thread_id>", views.thread_read_status, name="thread_read_status"),

    # Needed for translations in JavaScript
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),

    # Debug Routes
    path('__debug__/', include(debug_toolbar.urls)),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# in deployment serve files in the proper way
# see: https://docs.djangoproject.com/en/3.2/howto/static-files/deployment/
