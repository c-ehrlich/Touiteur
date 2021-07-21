from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

class UserPrefLocaleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.user.language:
            translation.activate(request.user.language)
            request.LANGUAGE_CODE = translation.get_language()
