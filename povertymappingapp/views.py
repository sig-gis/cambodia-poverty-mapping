from django.conf import settings
from django.shortcuts import redirect
from django.utils import translation

def switch_language(request):
    language = request.GET.get('language')
    next_url = request.GET.get('next', '/')
    
    if language and language in dict(settings.LANGUAGES).keys():
        # Set the language in the session
        request.session[translation.LANGUAGE_SESSION_KEY] = language
        # Optionally set the language as a cookie
        response = redirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response
    
    return redirect(next_url)
