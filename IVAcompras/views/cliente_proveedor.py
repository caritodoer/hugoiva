from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from cuentas.decorators import require_auth
from ..resources import CliProResource
from ..models import CliPro
from ..forms import CliProForm

from tablib import Dataset
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import logging

logger = logging.getLogger(__name__)


@require_auth
def exp_cli_pro(request):
    CliPro_resource = CliProResource()
    dataset = CliPro_resource.export()
    # para que guarde como csv: se puede abrir con excel
    response = HttpResponse(dataset.xls, content_type="text/xls")
    response["Content-Disposition"] = 'attachment; filename="clipro.xls"'
    # para que guarde como json
    # response = HttpResponse(dataset.json, content_type='application/json')
    # response['Content-Disposition'] = 'attachment; filename="persons.json"'
    return response


@require_auth
def imp_cli_pro(request):
    if request.method == "POST":
        CliPro_resource = CliProResource()
        dataset = Dataset()
        new_CliPro = request.FILES["myfile"]

        dataset.load(new_CliPro.read(), "xls")

        result = CliPro_resource.import_data(
            dataset, dry_run=True
        )  # Test the data import
        if not result.has_errors():
            CliPro_resource.import_data(dataset, dry_run=False)  # Actually import now
            return redirect("iva:l_cli_pro")
    context = {
        "title": "Importar Cliente-Proveedor",
    }
    return render(request, "importar.html", context)


@require_auth
def l_cli_pro(request):
    queryset = CliPro.objects.all().order_by("id")

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
        "title": "Clientes-Proveedores",
    }
    return render(request, "l_cli_pro.html", context)


@require_auth
def a_cli_pro(request):
    form = CliProForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    elif request.method == "POST":
        logger.debug("Error al validar el formulario: %s", form.errors)
    context = {
        "url": "/l_cli_pro",
        "title": "Alta de Cliente/Proveedor",
        "form": form,
    }
    return render(request, "altas.html", context)


@require_auth
def m_cli_pro(request, id=None):
    instance = get_object_or_404(CliPro, id=id)
    form = CliProForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    elif request.method == "POST":
        logger.debug("Error al validar el formulario: %s", form.errors)
    context = {
        "title": "Modificar Cliente/Proveedor",
        "instance": instance,
        "form": form,
        "url": "/l_cli_pro",
    }
    return render(request, "altas.html", context)


@require_auth
def v_cli_pro(request, id=None):
    instance = get_object_or_404(CliPro, id=id)
    context = {
        "instance": instance,
        "title": "Detalle de Cliente/Proveedor",
    }
    return render(request, "v_cli_pro.html", context)


@require_auth
def d_cli_pro(request, id=None):
    instance = get_object_or_404(CliPro, id=id)
    instance.delete()
    return redirect("iva:home")
