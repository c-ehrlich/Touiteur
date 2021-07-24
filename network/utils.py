from .models import User, Post, Conversation
from django.core.paginator import Paginator
import datetime
from pytz import timezone


# +-----------------------------------------+
# |           GLOBAL VARIABLES              |
# +-----------------------------------------+
# shouild probably factor these out in a more elegant way
PAGINATION_POST_COUNT = 10


# +-----------------------------------------+
# |          UTILITY FUNCTIONS              |
# +-----------------------------------------+
def check_username_validity(username):
    """CHECKS USERNAME VALIDITY
    
    input: username (string)
    output: boolean (true or false)
    
    conditions:
    The username must be at least 2 characters long
    The first character must be alphanumeric
    Every character after that must be either alphanumeric or underscore"""
    if len(username) < 2:
        return False
    if not username[0].isalnum():
        return False
    for character in username[1:]:
        if not (character.isalnum() or character == '_'):
            return False
    return True


def convert_javascript_date_to_python(js_date_now):
    """takes a javascript Date.now() value, and converts it to a Python datetime object
    
    input: javascript Date.now (epoch time)
    output: Python datetime object that represents the same time"""
    js_date_formatted = js_date_now / 1000
    utc = timezone('UTC')
    date = datetime.datetime.fromtimestamp(js_date_formatted, tz=utc)
    return date


def get_display_time(datetime_input):
    """Takes a datatime object, and returns a time difference string.
    
    input: a date, in datetime object format
    output: a string showing the amount of time that has elapsed
    
    Sample output strings:
    less than 1 minute:   'now'
    less than 1 hour:     '22m'
    less than 1 day:      '4h'
    this year:            'Mar 11'
    older:                'Mar 11, 2019'

    TODO: Localise this! 
    """
    utc = timezone('UTC')
    post = datetime_input
    now = datetime.datetime.now(tz=utc)
    difference = now - post
    td_days = difference.days
    td_secs = difference.seconds
    if td_days == 0 and td_secs < 60:
        return "now"
    if td_days == 0 and td_secs < 3600:
        return f"{td_secs // 60}m"
    if td_days == 0 and td_secs < 86400:
        return f"{td_secs // 3600}h"
    if post.year == now.year:
        return datetime.datetime.strftime(post, "%b %-d")
    if post.year != now.year:
        return datetime.datetime.strftime(post, "%b %-d, %Y")
    return "if you see this, there was an error in get_display_time"


def get_dm_threads_paginated(request):
    page = request.GET.get('page', 1)
    user = request.user
    objects = Conversation.objects.filter(user_ids__contains=[user.id])
    for object in objects:
        if object.user_ids[0] == user.id:
            object.convo_partner = User.objects.get(id=object.user_ids[1])
        else:
            object.convo_partner = User.objects.get(id=object.user_ids[0])
    # TODO get the nicely formatted timestamps
    print(objects)
    p = Paginator(objects, PAGINATION_POST_COUNT)
    return p.page(page) 


def get_mentions_from_post(post_text):
    """Takes a post text, and returns a list of mentions (User objects) in the post"""
    mentions = []
    for word in post_text.split():
        # compare the word to a regular expression:
        # the first character must be '@'
        # the second and third character must be alphanumeric
        # keep going until you reach a character that isn't alphanumeric or '_',
        # which means it's the end of the username
        length = len(word)
        if length >= 2:
            if word[0] == '@' and word[1].isalnum():
                # create a new string object that is the word without the '@'
                username = word[1]
                # then, keep adding characters to the new word until you hit a character that is neither alphanumeric nor '_'
                location = 2
                while location < length:
                    if word[location].isalnum() or word[location] == '_':
                        username += word[location]
                        location += 1
                    else:
                        break
                # if a user with that username exists, add it to the list
                try:
                    user = User.objects.get(username=username)
                    if not user in mentions:
                        print(mentions)
                        mentions.append(user)
                        user.mentions_since_last_checked += 1
                        user.save()
                    else:
                        print(mentions)
                except User.DoesNotExist:
                    pass
    return mentions


def get_posts_from_followed_accounts(request):
    page = request.GET.get('page', 1)
    user = request.user
    objects = Post.objects.filter(user__in=user.following.all())
    for object in objects:
        object.timestamp_f = get_display_time(object.timestamp)
    p = Paginator(objects, PAGINATION_POST_COUNT)
    return p.page(page)


def get_post_from_id(id):
    post = Post.objects.get(id=id)
    post.timestamp_f = get_display_time(post.timestamp)
    return post


def get_post_count_since_timestamp(request, timestamp, context):
    """returns the number of new posts for a given context since a given timestamp
    
    inputs: timestamp (python datetime object)
            context (dictionary)
    outputs: new_post_count (int)

    context options: 
        'location':
            'public_feed',
            'user',
            'following'
        'username': (this will not contain anything unless the posts from a user profile are being checked)
            '<username>'
    """
    user = request.user
    posts = {}
    if context['location'] == 'user':
        post_user = get_user_from_username(context['username'])
        # get posts by post_user, newer than timestamp
        posts = Post.objects.filter(user=post_user, timestamp__gte=timestamp)
    if context['location'] == 'public_feed':
        # get posts by all users, newer than timestamp
        posts = Post.objects.filter(timestamp__gt=timestamp)
    if context['location'] == 'following':
        # get posts by followed users, newer than timestamp
        posts = Post.objects.filter(user__in=user.following.all()).filter(timestamp__gt=timestamp)
    if context['location'] == 'index':
        posts = Post.objects.filter(timestamp__gt=timestamp)
    if context['location'] == 'mentions':
        posts = Post.objects.filter(mentioned_users__in=[user], timestamp__gt=timestamp)
    # if we haven't created posts yet, return an error
    if  posts:
        print(posts)
        return posts.count()
    else:
        return 0


def get_posts(request, username=None):
    """RETURNS A PAGE OF POSTS FROM A USER"""
    page = request.GET.get('page', 1)
    if username == None:
        objects = Post.objects.all()
    else:
        user = get_user_from_username(username)
        objects = Post.objects.filter(user=user).all()
    for object in objects:
        object.timestamp_f = get_display_time(object.timestamp)
    p = Paginator(objects, PAGINATION_POST_COUNT)
    return p.page(page)


def get_posts_with_mention(request, username):
    """RETURNS A PAGE OF POSTS THAT MENTION A USER"""
    page = request.GET.get('page', 1)
    user = get_user_from_username(username)
    # get all posts where the user is mentioned
    objects = Post.objects.filter(mentioned_users__in=[user])
    for object in objects:
        object.timestamp_f = get_display_time(object.timestamp)
    p = Paginator(objects, PAGINATION_POST_COUNT)
    return p.page(page)


def get_user_from_id(id):
    user = User.objects.get(id=id)
    return user

    
def get_user_from_username(username):
    user = User.objects.get(username=username)
    return user
