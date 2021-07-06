from .models import User, Post
from django.core.paginator import Paginator


# +-----------------------------------------+
# |           GLOBAL VARIABLES              |
# +-----------------------------------------+
# shouild probably factor these out in a more elegant way
PAGINATION_POST_COUNT = 10


# +-----------------------------------------+
# |          UTILITY FUNCTIONS              |
# +-----------------------------------------+
def get_post_from_id(id):
    post = Post.objects.get(id=id)
    return post


def get_posts(request, username=None):
    """RETURNS A PAGE OF POSTS FROM A USER"""
    page = request.GET.get('page', 1)
    if username == None:
        objects = Post.objects.all()
    else:
        user = get_user_from_username(username)
        objects = Post.objects.filter(user=user).all()
    p = Paginator(objects, PAGINATION_POST_COUNT)
    return p.page(page)


def get_user_from_username(username):
    user = User.objects.get(username=username)
    return user