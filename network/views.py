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
        "new_post_form": NewPostForm(auto_id=True)
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
# TODO remove csrf_exempt here
@csrf_exempt
def compose(request):
    data=json.loads(request.body)
    text = data.get("text", "")
    user=request.user
    print("TEST: " + text)
    post = Post(user=user, text=text)
    post.save()
    return JsonResponse({"message": "Post sent successfully"}, status=201)


def like(request, id):
    # get necessary data
    user = get_user_from_username(request.user.username)
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        print("we're putting!")
        user.liked_posts.add(post.id)
        user.save()
        return HttpResponse(status=204)


# TODO this doesn't work. figure out how to implement this.
# Options: 
#     1. just always slice the data manually
#     2. return a partial page and AJAX it in there
def paginated_posts(request, username=None, page=1):
    posts = get_posts(request, username, page)
    # return JsonResponse([posts.serialize() for post in posts], safe=False)
    # return JsonResponse(posts, safe=False)


def posts_public(request):
    post_list = Post.objects.all().values()
    paginator = Paginator(post_list, 10)
    posts = paginator.page(1)
    print(posts)
    print(type(posts))
    print(list(posts))
    return JsonResponse(list(posts), status=204, safe=False)
    # return JsonResponse("{'posts': [{'1':'a'},{'2':'b'}]}", safe=False)