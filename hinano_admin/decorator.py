from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseNotFound
from django.urls import reverse,reverse_lazy
from django.db.models import Q,Count,Case, CharField, Value, When,IntegerField,Sum,Avg
from django.http import Http404

import functools

def is_login(arg1):
    def decorator(function):
        # @login_required
        @functools.wraps(function)
        def wrap(request,*args, **kwargs):
            # have = False
            try:
            # if arg1 == 'OrderBasket':
            #     have = OrderBasket.objects.filter(store=request.user.store).exists()
                if request.session['email'] : 
                    return function(request, *args, **kwargs)
                else    : 
                    return HttpResponseRedirect(reverse_lazy('login'))
            except:
                return HttpResponseRedirect(reverse_lazy('login'))
        return wrap
    return decorator