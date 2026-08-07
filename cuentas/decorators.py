from functools import wraps
from django.http import Http404

def require_auth(f):
    @wraps(f)
    def funcion_decorada(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        return f(request, *args, **kwargs)

    return funcion_decorada