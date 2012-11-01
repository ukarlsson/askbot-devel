from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseNotAllowed
from django.contrib.auth import authenticate, login, logout
from askbot.utils.decorators import get_only
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

@get_only
def ida_login(request, equa_id, password):
    user = authenticate(equa_id=equa_id, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render_to_response(
                    'registration/login_ida_failure.html', {
                        'error' : 'User not active.'
                    }
                )
    else:
        return render_to_response(
                'registration/login_ida_failure.html', {
                    'error' : 'Authentication failed.'
                }
            )


@get_only
def ida_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
