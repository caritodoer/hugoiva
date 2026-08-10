from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from cuentas.decorators import require_auth

from ..models import Libro, Detalle, Empresa
from ..forms import LibroForm

import logging

logger = logging.getLogger(__name__)


@require_auth
def a_libro(request, k=None, v=None):
    empresa = get_object_or_404(Empresa, id=k)
    tipo_libro = v
    instance = Libro(empresa=empresa, tipo_libro=tipo_libro)
    instance.save()
    return HttpResponseRedirect(instance.get_absolute_url())


@require_auth
def m_libro(request, id=None):
    instance = get_object_or_404(Libro, id=id)
    form = LibroForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    elif request.method == "POST":
        logger.debug("Error al validar el formulario: %s", form.errors)
    context = {
        "title": "Modificar Libro",
        "instance": instance,
        "form": form,
    }
    return render(request, "altas.html", context)


@require_auth
def v_libro(request, id=None):
    instance = get_object_or_404(Libro, id=id)
    list_detalle = (
        Detalle.objects.all()
        .order_by("-fecha", "-tipo_comprobante", "letra", "-nfactura")
        .filter(libro=instance)
    )
    imp_x_det = {}
    for d in list_detalle:
        importe = (
            d.gravado
            + d.no_gravado
            + d.iva21
            + d.iva105
            + d.iva_otros
            + d.rg2126
            + d.ret_IVA
            + d.ret_iibb
            + d.imp_int
            + d.otros
        )
        imp_x_det[d.id] = importe

    desde = request.GET.get("d")
    hasta = request.GET.get("h")

    if desde and hasta:
        list_detalle = list_detalle.filter(fecha__range=(desde, hasta))

    paginator = Paginator(list_detalle, 10)  # Show 25 DetAna_queryset per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset_list = paginator.page(paginator.num_pages)

    context = {
        "page_request_var": page_request_var,
        "object_list": queryset_list,
        "list_detalle": queryset_list,
        "imp_x_det": imp_x_det,
        "instance": instance,
        "title": "Libro",
    }
    return render(request, "v_libro.html", context)


@require_auth
def l_libro(request):
    list_emp = Empresa.objects.all().order_by("-id")
    list_libros = Libro.objects.all()

    # libros
    lib_x_emp = {}
    for e in list_emp:
        k = e
        list_lxe = ["X", "X"]  # listado de libros por empresa
        for l in list_libros:
            if e == l.empresa:
                if l.tipo_libro == "V":
                    list_lxe[0] = l
                if l.tipo_libro == "C":
                    list_lxe[1] = l
        lib_x_emp[k] = list_lxe

    context = {
        "object_list_empresa": list_emp,
        "object_dict_libro": lib_x_emp,
        "title": "Listado de Libros",
    }
    return render(request, "l_libro.html", context)


@require_auth
def d_libro(request, id=None):
    instance = get_object_or_404(Libro, id=id)
    instance.delete()
    return redirect("iva:home")
