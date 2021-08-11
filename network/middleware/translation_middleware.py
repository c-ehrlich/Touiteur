from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

class UserPrefLocaleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if request.user.language and not request.path in ("/register2", "/register3"):
            # if we're not on register2 or register3
                translation.activate(request.user.language)
                request.LANGUAGE_CODE = translation.get_language()
