from .models import User, Post
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
    print("running username check")
    if len(username) < 2:
        return False
    if not username[0].isalnum():
        return False
    for character in username[1:]:
        if not (character.isalnum() or character == '_'):
            return False
    print(f"{username} is valid")
    return True


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