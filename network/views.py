import json
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _lazy

from network.forms import EditAccountForm, NewPostForm, RegisterAccountForm, RegisterAccountStage2Form, RegisterAccountStage3Form
from network.models import User, Post, Conversation
from network import utils

# TODO temp imports remove later
from django.views.decorators.csrf import csrf_exempt, csrf_protect


# +-----------------------------------------+
# |        VIEWS THAT RETURN PAGES          |
# +-----------------------------------------+

@login_required
def account(request):
    user = request.user

    if request.method == "GET":
        return render(request, "network/account.html", {
            "form": EditAccountForm(instance = user)
    })
    if request.method == "POST":
        form = EditAccountForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            user = authenticate(
                request, 
                username=utils.get_user_from_id(request.user.id), 
                password=form.cleaned_data["password"]
            )
            if user is None:
                return render(request, "network/account.html", {
                    "form": EditAccountForm(instance = utils.get_user_from_id(request.user.id)),
                    "message": _("Invalid password.")
                })
            if utils.check_username_validity(form.cleaned_data["username"]) == False:
                user = utils.get_user_from_id(request.user.id) # dirty hack to clean the username field TODO refactor
                # return an EditAccountForm with the user's original information
                return render(request, "network/account.html", {
                    "form": EditAccountForm(instance = user),
                    "message": _("Username is not valid."),
                })

            # get new_password and new_pass_confirm from form
            # check if they are the same, if so change the password
            # if not, return an EditAccountForm with the user's original information
            # and a message saying the passwords don't match
            new_password = form.cleaned_data["new_password"]
            new_password_confirm = form.cleaned_data["new_password_confirm"]
            if new_password != new_password_confirm:
                return render(request, "network/account.html", {
                    "form": EditAccountForm(instance = user),
                    "message": _("New passwords don't match.")
                })
            if new_password != None and new_password != "":
                user.set_password(new_password)
                user.save()

            form.save()

        # form is not valid
        else:
            print(form.data)
            return render(request, "network/account.html", {
                "form": EditAccountForm(instance = user),
                "message": _("Form data is invalid")
            })
        print("everything went good!")
        return render(request, "network/account.html", {
            "form": EditAccountForm(instance = utils.get_user_from_id(request.user.id))
        })


@login_required
def dms(request):
    threads = utils.get_dm_threads_paginated(request)
    return render(request, "network/dms.html", {
        "threads": threads,
    })


@login_required
def dm_thread(request, username):
    convo_partner = utils.get_user_from_username(username)
    page = request.GET.get('page', 1)
    user_id = request.user.id
    convo_partner_id = convo_partner.id
    conversation = Conversation.objects.get(
        user_ids=[user_id, convo_partner_id]
    )
    thread = conversation.messages.all()
    p = Paginator(thread, utils.PAGINATION_POST_COUNT)
    # TODO if thread doesn't exist, give error
    return render(request, "network/dm_thread.html", {
        "thread": p.page(page),
        "thread_id": conversation.id,
    })


@login_required
def following(request):
    posts = utils.get_posts_from_followed_accounts(request)
    return render(request, "network/following.html", {
        "posts": posts,
    })


def index(request):
    """RETURNS THE INDEX PAGE"""
    if request.method == "GET":
        posts = utils.get_posts(request)
        return render(request, "network/index.html", {
            "posts": posts,
            "new_post_form": NewPostForm(auto_id=True),
        })
    else:
        return JsonResponse({
            "error": "GET request required"
        }, 400)


def likes(request, username):
    """RETURNS THE LIKED POSTS PAGE"""
    if request.method == "GET":
        view_user = utils.get_user_from_username(username)
        page = request.GET.get('page', 1)
        if view_user.show_liked_posts == True:
            posts = utils.get_liked_posts_paginated(request, view_user)
        else:
            return render(request, "network/likes.html", {
                "view_user": view_user,
            })
            # TODO return a view that shows that the user has sharing likes off
        return render(request, "network/likes.html", {
            "view_user": view_user,
            "posts": posts,
        })
    else:
        return JsonResponse({
            "error": "GET request required"
        }, 400)


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
                "message": _("Invalid username and/or password."),
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def mentions(request):
    user = request.user
    if request.method == "GET":
        return render(request, "network/mentions.html", {
            "posts": utils.get_posts_with_mention(request, user.username),
        })
    else:
        return HttpResponseRedirect(reverse("index"))


def post(request, id):
    post = utils.get_post_from_id(request, id)
    # TODO do something if it's a bad post


    replies = utils.get_posts(request, reply_to=post)
    return render(request, "network/post.html", {
        "post": post,
        "posts": replies 
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        displayname = request.POST["displayname"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": _("Passwords must match."),
                "form": RegisterAccountForm(),
            })

        if not utils.check_username_validity(username):
            return render(request, "network/register.html", {
                "message": _("Username is not valid."),
                "form": RegisterAccountForm(),
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.displayname = displayname
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": _("Username already taken."),
                "form": RegisterAccountForm(),
            })
        login(request, user)
        return HttpResponseRedirect(reverse("register2"))
    else:
        return render(request, "network/register.html", {
            "form": RegisterAccountForm()
        })


@login_required
def register2(request):
    user = request.user
    if request.method == "GET":
        if user.has_completed_onboarding == False:
            return render(request, "network/register2.html", {
                "form": RegisterAccountStage2Form(instance = user)
            })
        else:
            return HttpResponseRedirect(reverse("index"))
    if request.method == "POST":
        form = RegisterAccountStage2Form(request.POST, request.FILES, instance = user)
        if form.is_valid():
            user.bio = form.cleaned_data['bio']
            user.avatar = form.cleaned_data['avatar']
            form.save()
            return HttpResponseRedirect(reverse("register3"))
        else:
            return render(request, "network/register2.html", {
                "form": form,
                "message": _("Form data is invalid")
            })


@login_required
def register3(request):
    user = request.user
    if request.method == "GET":
        if user.has_completed_onboarding == False:
            return render(request, "network/register3.html", {
                "form": RegisterAccountStage3Form(instance = user)
            })
        else:
            return HttpResponseRedirect(reverse("index"))
    if request.method == "POST":
        form = RegisterAccountStage3Form(request.POST, instance = user)
        if form.is_valid():
            user.theme = form.cleaned_data['theme']
            user.language = form.cleaned_data['language']
            user.show_liked_posts = form.cleaned_data['show_liked_posts']
            user.has_completed_onboarding = True
            user.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/register3.html", {
                "form": form,
                "message": _("Form data is invalid")
            })


@login_required
def user(request, username):
    request.view_user = utils.get_user_from_username(username)
    posts = utils.get_posts(request, username)
    if request.user == request.view_user:
        return render(request, "network/user.html", {
            "view_user": request.view_user,
            "posts": posts,
            "new_post_form": NewPostForm(),
        })
    else:
        return render(request, "network/user.html", {
            "view_user": user,
            "posts": posts,
        })


# +-----------------------------------------+
# |        VIEWS THAT RETURN JSON           |
# +-----------------------------------------+
@csrf_protect
def clear_mentions_count(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        if data['intent'] == 'clear_mentions_count':
            user = request.user
            user.mentions_since_last_checked = 0
            user.save()
            return HttpResponse(status=200)
        else:
            print(data['intent'])
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)


@csrf_protect
def compose(request):
    print(request.headers)
    form = NewPostForm(request.POST)
    if form.is_valid():
        post_text = form.cleaned_data["post_text"]
        if post_text == "":
            return JsonResponse({
                "message": _("You can't submit an empty post")
            }, status=400)
        user=request.user
        mentioned_users = utils.get_mentions_from_post(post_text)
        post = Post(user=user, text=post_text)
        post.save()
        for user in mentioned_users:
            post.mentioned_users.add(user)
        return HttpResponseRedirect(request.headers['Referer'])
    else:
        return JsonResponse({
            "message": _("Form data invalid")
        }, status=400)


@csrf_protect
def edit(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        new_text = data['new_text']
        if len(new_text) > 140:
            return JsonResponse({
                "message": _("Maximum post length is 140 characters"),
                "edited": False,
            }, status=400)
        post = utils.get_post_from_id(request, post_id)
        if request.user == post.user:
            post.text = new_text
            post.save()
            return JsonResponse({
                "message": _("Post edited successfully"),
                "edited": True,
            }, status=201)
        else:
            return JsonResponse({
                "message": _("You are not authorized to edit this post"),
                "edited": False,
            }, status=400)


@csrf_protect
def follow(request, user_id):
    if request.method == "PUT":
        user = request.user
        # user is trying to follow themselves
        if user_id == user.id:
            return JsonResponse({
                "error": _("You cannot follow your own account.")
            }, status=400)
        else: 
            data = json.loads(request.body)
            user_to_follow = User.objects.get(id=user_id) 
            # good follow request
            if data['intent'] == 'follow' and user_to_follow not in user.following.all():
                user.following.add(user_to_follow)
                return JsonResponse({
                    "message": _(f"followed user {user_to_follow}")
                }, status=201)
            # good unfollow request
            if data['intent'] == 'unfollow' and user_to_follow in user.following.all():
                print("you are currently following this user")
                user.following.remove(user_to_follow)
                return JsonResponse({
                    "message": _(f"unfollowed user {user_to_follow}")
                }, status=201)
            # We reach this page if the intent does not match the current follow status
            return JsonResponse({
                "error": _("follow intent does not match current follow state")
            }, status=400)
    # user did not make a put request
    else:
        return JsonResponse({
            "error": _("PUT request required.")
        }, status=400)


@csrf_protect
def get_notifications(request):
    if request.method == "PUT":
        user = request.user
        if user == None:
            return JsonResponse({
                "error": _("You are not logged in.")
            }, status=400)
        # build a JSON response that contains any notifications
        # (for now just unread mentions, but might add more stuff ie DMs later)
        # maybe also a total count of notifications, for app badge etc?
        return JsonResponse({
            "mention_count": user.mentions_since_last_checked
        }, status=200)
    else:
        return JsonResponse({
            "error": _("PUT request required.")
        }, status=400)


@csrf_protect
def like(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        user = request.user
        post = utils.get_post_from_id(request, post_id)
        if data['like'] == True:
            user.liked_posts.add(post)
            return JsonResponse({
                "message": _("Post liked successfully"),
                "post_id": post_id,
                "is_liked": True,
                "like_count": post.users_who_liked.count(),
                }, status=201)
        elif data['like'] == False:
            user.liked_posts.remove(post)
            return JsonResponse({
                "message": _("Post unliked successfully"),
                "post_id": post_id,
                "is_liked": False,
                "like_count": post.users_who_liked.count(),
                }, status=201)
    else:
        print("ERROR please only come here via PUT")
        return JsonResponse({
            "error": _("PUT request required.")
        }, status=400)


def new_posts(request):
    """checks for new post count
    expects a json object in the request. that object should contain a 'context' variable. inside that variable:
        'location': can be 'public_feed', 'user', or 'following' (can add more later for different views)
        if 'location' == 'user':
            'username': the username of the user who we are checking for new posts
    returns a JsonResponse with the key 'count' which is the new post count
    """
    if request.method == "PUT":
        data = json.loads(request.body)
        datetime_obj = utils.convert_javascript_date_to_python(data['timestamp'])
        new_post_count = utils.get_post_count_since_timestamp(request, datetime_obj, data['context'])
        return JsonResponse({
            "new_post_count": new_post_count,
        }, status=201)
    else:
        return JsonResponse({
            "error": _("GET request required.")
        }, status=400)


@csrf_protect
def reply(request, post_id):
    print(request.headers)
    if request.method == "PUT":
        data = json.loads(request.body)
        text = data["text"]
        user = request.user
        post = utils.get_post_from_id(request, post_id)
        reply = Post(user=user, text=text, reply_to=post)
        reply.save()
        # maybe factor out the mentioned users thing? TODO
        mentioned_users = utils.get_mentions_from_post(text)
        for user in mentioned_users:
            reply.mentioned_users.add(user)
        # this is the reply count that updates on the website, for the post that is being replied to
        reply_count = post.replies.count()
        return JsonResponse({
            "reply_count": reply_count,
        }, status=201)
    else:
        return JsonResponse({
            "error": _("PUT request required.")
        }, status=400)


@csrf_protect
def thread_read_status(request, thread_id):
    """marks all unread DMs in a thread as read"""
    if request.method == "PUT":
        thread = Conversation.objects.get(id=thread_id)
        # TODO make sure the user is actually in the thread
        try:
            for message in thread.messages.all():
                if message.recipient == request.user and message.is_read == False:
                    message.is_read = True
                    message.save()
            return JsonResponse({
                "message": _("All posts marked as read")
            }, status=201)
        except Exception:
            return JsonResponse({
                "error": _("Error setting thread to read")
            }, status=500)
    else:
        return JsonResponse({
            "error": _("PUT request required")
        }, status=400)