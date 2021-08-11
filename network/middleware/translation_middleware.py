from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

class UserPrefLocaleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.user.language:
            # if we're not on register2 or register3
            if request.path is not "/register2" and not "/register3":
                translation.activate(request.user.language)
                request.LANGUAGE_CODE = translation.get_language()
