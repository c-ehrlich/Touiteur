import json
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post
from .utils import get_user_from_username, get_post_from_id, get_posts

# TODO temp imports remove later
from django.views.decorators.csrf import csrf_exempt


# +-----------------------------------------+
# |                  FORMS                  |
# +-----------------------------------------+

class NewPostForm(forms.Form):
    pass
    post_text = forms.CharField(
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
    posts = get_posts(request)
    return render(request, "network/index.html", {
        "posts": posts,
        "new_post_form": NewPostForm(auto_id=True),
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


def post(request, id):
    post = get_post_from_id(id)
    # TODO do something if it's a bad post
    return render(request, "network/post.html", {
        "post": post
    })


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
    posts = get_posts(request, username)
    return render(request, "network/user.html", {
        "view_user": user,
        "posts": posts
    })


# +-----------------------------------------+
# |        VIEWS THAT RETURN JSON           |
# +-----------------------------------------+
# TODO remove csrf_exempt here and everywhere
@csrf_exempt
def compose(request):
    data=json.loads(request.body)
    text = data.get("text", "")
    user=request.user
    print("TEST: " + text)
    post = Post(user=user, text=text)
    post.save()
    return JsonResponse({"message": "Post sent successfully"}, status=201)


@csrf_exempt
def edit(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        new_text = data['new_text']
        # TODO run some checks on new_text (length etc)?
        post = get_post_from_id(post_id)
        if request.user == post.user:
            post.text = new_text
            post.save()
            return JsonResponse({
                "message": "Post edited successfully",
            }, status=201)
        else:
            return JsonResponse({
                "message": "You are not authorized to edit this post",
            }, status=400)


@csrf_exempt
def like(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        user = request.user
        post = get_post_from_id(post_id)
        if data['like'] == True:
            user.liked_posts.add(post)
            return JsonResponse({
                "message": "Post liked successfully",
                "post_id": post_id,
                "is_liked": True,
                "like_count": post.users_who_liked.count(),
                }, status=201)
        elif data['like'] == False:
            user.liked_posts.remove(post)
            return JsonResponse({
                "message": "Post unliked successfully",
                "post_id": post_id,
                "is_liked": False,
                "like_count": post.users_who_liked.count(),
                }, status=201)
    else:
        print("ERROR please only come here via PUT")
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
