from .models import User, Post

def get_user_from_username(username):
    user = User.objects.get(username=username)
    return user