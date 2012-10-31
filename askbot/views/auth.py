from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseNotAllowed
from django.contrib.auth import authenticate, login
from askbot.utils.decorators import get_only
from django.core.urlresolvers import reverse

@get_only
def ida_login(request, equa_id, password):
    user = authenticate(equa_id=equa_id, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))
