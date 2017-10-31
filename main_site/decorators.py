from django.core.exceptions import PermissionDenied


def is_not_priveleged(user):
    if user.groups.filter(name='TransportStaff').exists():
        return False

    if user.groups.filter(name='TransportAdmin').exists():
        return False

    return True

def check_not_priveleged(function):
    def wrap(request, *args, **kwargs):
        user=request.user
        if is_not_priveleged(user):
            raise PermissionDenied()
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap