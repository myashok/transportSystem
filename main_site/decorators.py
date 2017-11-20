from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from main_site.models import Request, Bill


def is_not_priveleged(user):
    if user.groups.filter(name='TransportStaff').exists():
        return False

    if user.groups.filter(name='TransportAdmin').exists():
        return False

    return True

def check_priveleged(function):
    def wrap(request, *args, **kwargs):
        user=request.user
        if is_not_priveleged(user):
            raise PermissionDenied()
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap



def check_owner_of_request(function):
    def wrap(request, *args, **kwargs):
        req = get_object_or_404(Request, pk=kwargs['pk'])
        if req.user!=request.user:
            raise PermissionDenied()
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def check_owner_of_bill(function):
    def wrap(request, *args, **kwargs):
        req = get_object_or_404(Request, pk=kwargs['pk'])
        if is_not_priveleged(request.user) and request.user!=req.user:
            raise PermissionDenied()
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap