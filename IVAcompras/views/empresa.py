from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from cuentas.decorators import require_auth
from ..resources import EmpresaResource
from ..models import Empresa
from ..forms import EmpresaForm

from tablib import Dataset

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import logging

logger = logging.getLogger(__name__)


@require_auth
def exp_empresa(request):
    empresa_resource = EmpresaResource()
    dataset = empresa_resource.export()
    # para que guarde como csv: se puede abrir con excel
    response = HttpResponse(dataset.xls, content_type="text/xls")
    response["Content-Disposition"] = 'attachment; filename="empresa.xls"'
    # para que guarde como json
    # response = HttpResponse(dataset.json, content_type='application/json')
    # response['Content-Disposition'] = 'attachment; filename="persons.json"'
    return response


@require_auth
def imp_empresa(request):
    if request.method == "POST":
        empresa_resource = EmpresaResource()
        dataset = Dataset()
        new_empresa = request.FILES["myfile"]

        dataset.load(new_empresa.read(), "xls")

        result = empresa_resource.import_data(
            dataset, dry_run=True
        )  # Test the data import
        if not result.has_errors():
            empresa_resource.import_data(dataset, dry_run=False)  # Actually import now
            return redirect("iva:l_empresa")
    context = {
        "title": "Importar Empresa",
    }
    return render(request, "importar.html", context)


@require_auth
def l_empresa(request):
    queryset = Empresa.objects.all().order_by("id")
    query = request.GET.get("q")
    if query:
        queryset = queryset.filter(nombre__icontains=query)

    paginator = Paginator(queryset, 15)  # Show 25 DetAna_queryset per page
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
        "title": "Empresas",
    }
    return render(request, "l_empresa.html", context)


@require_auth
def a_empresa(request):
    form = EmpresaForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        return HttpResponseRedirect(instance.get_absolute_url())
    elif request.method == "POST":
        logger.debug("Error al validar el formulario: %s", form.errors)
    context = {
        "url": "/l_empresa",
        "title": "Nueva Empresa",
        "form": form,
    }
    return render(request, "altas.html", context)


@require_auth
def m_empresa(request, id=None):
    instance = get_object_or_404(Empresa, id=id)
    form = EmpresaForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    elif request.method == "POST":
        logger.debug("Error al validar el formulario: %s", form.errors)
    context = {
        "url": "/l_empresa",
        "title": "Modificar Empresa",
        "instance": instance,
        "form": form,
    }
    return render(request, "altas.html", context)


@require_auth
def v_empresa(request, id=None):
    instance = get_object_or_404(Empresa, id=id)
    context = {
        "instance": instance,
        "title": "Detalle de Empresa",
    }
    return render(request, "v_empresa.html", context)


@require_auth
def d_empresa(request, id=None):
    instance = get_object_or_404(Empresa, id=id)
    instance.delete()
    return redirect("iva:home")
