from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict

from cuentas.decorators import require_auth

from ..models import Libro, Detalle
from ..forms import DetalleForm

import logging

logger = logging.getLogger(__name__)


@require_auth
def a_detalle(request, l=None):
    libro = get_object_or_404(Libro, id=l)
    instance = Detalle(libro=libro)
    # instance.save()
    form = DetalleForm(request.POST or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    elif request.method == "POST":
        logger.debug("Error al validar el formulario: %s", form.errors)
    context = {
        "libro": libro,
        "title": "Alta de Detalle",
        "form": form,
        "titulo2": "Alta Cliente-Proveedor",
        "url": "/v_libro/" + l,
    }
    return render(request, "altas.html", context)


@require_auth
def m_detalle(request, id=None):
    instance = get_object_or_404(Detalle, id=id)
    form = DetalleForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    elif request.method == "POST":
        logger.debug("Error al validar el formulario: %s", form.errors)
    l = str(instance.libro.id)
    context = {
        "title": "Modificar Detalle",
        "instance": instance,
        "form": form,
        "url": "/v_libro/" + l,
    }
    return render(request, "altas.html", context)


@require_auth
def v_detalle(request, id=None):
    instance = get_object_or_404(Detalle, id=id)
    objeto = DetalleForm(
        data=model_to_dict(Detalle.objects.get(id=id), exclude=["libro"])
    )
    context = {
        "instance": instance,
        "title": "Detalle de Detalle",
        "objeto": objeto,
    }
    return render(request, "v_detalle.html", context)


@require_auth
def d_detalle(request, id=None):
    instance = get_object_or_404(Detalle, id=id)
    id_libro = instance.libro.id
    instance.delete()
    return redirect("iva:v_libro", id=id_libro)
