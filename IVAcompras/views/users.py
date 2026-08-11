from cuentas.decorators import require_auth
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()


@require_auth
def usuarios(request):

    queryset = User.objects.all()
    context = {"object_list": queryset, "title": "Usuarios"}
    return render(request, "usuarios.html", context)
