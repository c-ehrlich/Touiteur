from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post
from .utils import get_user_from_username


# +-----------------------------------------+
# |           GLOBAL VARIABLES              |
# +-----------------------------------------+
# shouild probably factor these out in a more elegant way
PAGINATION_POST_COUNT = 10


# +-----------------------------------------+
# |                  FORMS                  |
# +-----------------------------------------+

class NewPostForm(forms.Form):
    post = forms.CharField(
        label = "New Post",
        max_length = 500,
        required=True,
        widget=forms.Textarea(attrs={
            'rows':3
        })
    )


# +-----------------------------------------+
# |        VIEWS THAT RETURN PAGES          |
# +-----------------------------------------+

def index(request):
    """RETURNS THE INDEX PAGE"""
    posts = paginated_posts(request)
    return render(request, "network/index.html", {
        "posts": posts
    })


def login_view(request):
    """RETURNS THE LOGIN VIEW"""
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def user(request, username):
    user = get_user_from_username(username)
    request.view_user = user
    posts = paginated_posts(request, user)
    return render(request, "network/user.html", {
        "view_user": user,
        "posts": posts
    })


# +-----------------------------------------+
# |        VIEWS THAT RETURN DATA           |
# +-----------------------------------------+
# factor these out to utils or some other file?

# def paginated_posts(request):
#     """RETURNS A PAGE OF POSTS FROM THE PUBLIC TIMELINE"""
#     page = request.GET.get('page', 1)
#     objects = Post.objects.all()
#     p = Paginator(objects, PAGINATION_POST_COUNT)
#     return p.page(page)


# def paginated_posts(request, user):
#     """RETURNS A PAGE OF POSTS FROM A USER"""
#     page = request.GET.get('page', 1)
#     objects = Post.objects.filter(user=user).all()
#     p = Paginator(objects, PAGINATION_POST_COUNT)
#     return p.page(page)

def paginated_posts(request, user=None, page=1):
    """RETURNS A PAGE OF POSTS FROM A USER"""
    print(user)
    print(type(user))
    # page = request.GET.get('page', 1)
    if user == None:
        objects = Post.objects.all()
    else:
        objects = Post.objects.filter(user=user).all()
    p = Paginator(objects, PAGINATION_POST_COUNT)
    return p.page(page)
