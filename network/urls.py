from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    # View Routes
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("post/<int:id>", views.post, name="post"),
    path("register", views.register, name="register"),
    path("user/<str:username>", views.user, name="user"),

    # API Routes
    path("compose", views.compose, name="compose"),
    path("like/<int:id>", views.like, name="like"),
    path("paginated_posts/<str:username>/<int:page>", views.paginated_posts, name="paginated_posts"),
    path("posts_public", views.posts_public, name="posts_public"),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# TODO in deployment serve files in the proper way
# see: https://docs.djangoproject.com/en/3.2/howto/static-files/deployment/
