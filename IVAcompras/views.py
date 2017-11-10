from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

"""
vistas:
- Empresas: AMVD
- Cliente-Proveedor : AMVD
- Libros : AMVD
	- Listado de libros vta filtrados por empresa
	- Listado de libros compra filtrados por empresa 
y periodo
- previsualizacion de la hoja del libro 
"""
from .resources import *
from tablib import Dataset

# Create your views here.

def exp_empresa(request):
    empresa_resource = EmpresaResource()
    dataset = empresa_resource.export()
    # para que guarde como csv: se puede abrir con excel 
    response = HttpResponse(dataset.xls, content_type='text/xls')
    response['Content-Disposition'] = 'attachment; filename="empresa.xls"'
    # para que guarde como json
    #response = HttpResponse(dataset.json, content_type='application/json')
    #response['Content-Disposition'] = 'attachment; filename="persons.json"'
    return response
def imp_empresa(request):
    if request.method == 'POST':
        empresa_resource = EmpresaResource()
        dataset = Dataset()
        new_empresa = request.FILES['myfile']

        imported_data = dataset.load(new_empresa.read(), "xls")

        result = empresa_resource.import_data(dataset, dry_run=True)  # Test the data import
        if not result.has_errors():
            empresa_resource.import_data(dataset, dry_run=False)  # Actually import now
            return redirect("iva:l_empresa")
    context = {
    	"title": "Importar Empresa",
	}
    return render(request, 'importar.html', context)

def exp_cli_pro(request):
    CliPro_resource = CliProResource()
    dataset = CliPro_resource.export()
    # para que guarde como csv: se puede abrir con excel 
    response = HttpResponse(dataset.xls, content_type='text/xls')
    response['Content-Disposition'] = 'attachment; filename="clipro.xls"'
    # para que guarde como json
    #response = HttpResponse(dataset.json, content_type='application/json')
    #response['Content-Disposition'] = 'attachment; filename="persons.json"'
    return response
def imp_cli_pro(request):
    if request.method == 'POST':
        CliPro_resource = CliProResource()
        dataset = Dataset()
        new_CliPro = request.FILES['myfile']

        imported_data = dataset.load(new_CliPro.read(), "xls")

        result = CliPro_resource.import_data(dataset, dry_run=True)  # Test the data import
        if not result.has_errors():
            CliPro_resource.import_data(dataset, dry_run=False)  # Actually import now
            return redirect("iva:l_cli_pro")
    context = {
    	"title": "Importar Cliente-Proveedor",
	}
    return render(request, 'importar.html', context)

# def exp_detalle(request):
#     detalle_resource = DetalleResource()
#     dataset = detalle_resource.export()
#     # para que guarde como csv: se puede abrir con excel 
#     response = HttpResponse(dataset.xls, content_type='text/xls')
#     response['Content-Disposition'] = 'attachment; filename="libro.xls"'
#     # para que guarde como json
#     #response = HttpResponse(dataset.json, content_type='application/json')
#     #response['Content-Disposition'] = 'attachment; filename="persons.json"'
#     return response
# def imp_detalle(request):
#     if request.method == 'POST':
#         detalle_resource = DetalleResource()
#         dataset = Dataset()
#         new_detalle = request.FILES['myfile']

#         imported_data = dataset.load(new_detalle.read(), "xls")

#         result = detalle_resource.import_data(dataset, dry_run=True)  # Test the data import
#         if not result.has_errors():
#             detalle_resource.import_data(dataset, dry_run=False)  # Actually import now
#             return redirect("iva:l_libro")
#     context = {
#     	"title": "Importar Libro",
# 	}
#     return render(request, 'importar.html', context)


def home(request):
	querysetCliPro=CliPro.objects.all().order_by('-id')
	list_emp=Empresa.objects.all().order_by('-id')
	list_libros=Libro.objects.all()

	#libros
	lib_x_emp={}
	for e in list_emp:
		k=e
		list_lxe=['X', 'X'] #listado de libros por empresa
		for l in list_libros:
			if e == l.empresa:
				if l.tipo_libro == 'V':
					list_lxe[0]=l
				if l.tipo_libro == 'C':
					list_lxe[1]=l
		lib_x_emp[k]=list_lxe	
	print(lib_x_emp)

	context = {
		"object_list_empresa": list_emp,
		"object_list_clipro": querysetCliPro,
		"object_dict_libro": lib_x_emp,
		"title": "Libros IVA Ventas / Compras",
	}	
	return render(request, "home.html", context)

# EMPRESA
def l_empresa(request):
	queryset = Empresa.objects.all().order_by('id')
	query = request.GET.get("q")
	if query:
		queryset = queryset.filter(nombre__icontains=query)

	paginator = Paginator(queryset, 15) # Show 25 DetAna_queryset per page
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
		"title": "Empresas"
	}
	return render(request, "l_empresa.html", context)
def a_empresa(request):
	form = EmpresaForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

		
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print (form.errors)
	context = {
		"url": "/l_empresa",
		"title" : "Nueva Empresa",
		"form": form,
	}
	return render(request, "altas.html", context)
def m_empresa(request, id=None):
	instance = get_object_or_404(Empresa, id=id)
	form = EmpresaForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print (form.errors)
	context = {
		"title" : "Modificar Empresa",
		"instance" : instance,
		"form" : form,
	}
	return render(request, "altas.html", context)
def v_empresa(request, id=None):
	instance = get_object_or_404(Empresa, id=id)
	context = {
		"instance" : instance,
		"title": "Detalle de Empresa",
	}
	return render(request, "v_empresa.html", context)
def d_empresa(request, id=None):
	instance = get_object_or_404(Empresa, id=id)
	instance.delete()
	return redirect("iva:home")

def a_cp_modal(request):
	form = CliProForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print (form.errors)
	context = {
		"title" : "Alta de Cliente/Proveedor",
		"form": form,
	}
	return render(request, "a_cp_modal.html", context)

# Cliente/Proveedor
def l_cli_pro(request):
	queryset = CliPro.objects.all().order_by('id')
	
	query = request.GET.get("q")
	if query:
		queryset = queryset.filter(nombre__icontains=query)

	paginator = Paginator(queryset, 15) # Show 25 DetAna_queryset per page
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
		"title": "Clientes-Proveedores"
	}
	return render(request, "l_cli_pro.html", context)
def a_cli_pro(request):
	form = CliProForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print (form.errors)
	context = {
		"url": "/l_cli_pro",
		"title" : "Alta de Cliente/Proveedor",
		"form": form,
	}
	return render(request, "altas.html", context)
def m_cli_pro(request, id=None):
	instance = get_object_or_404(CliPro, id=id)
	form = CliProForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print (form.errors)
	context = {
		"title" : "Modificar Cliente/Proveedor",
		"instance" : instance,
		"form" : form,
	}
	return render(request, "altas.html", context)
def v_cli_pro(request, id=None):
	instance = get_object_or_404(CliPro, id=id)
	context = {
		"instance" : instance,
		"title": "Detalle de Cliente/Proveedor",
	}
	return render(request, "v_cli_pro.html", context)
def d_cli_pro(request, id=None):
	instance = get_object_or_404(CliPro, id=id)
	instance.delete()
	return redirect("iva:home")

# Libro 

def a_libro(request, k=None, v=None):
	empresa = get_object_or_404(Empresa, id=k)
	tipo_libro = v
	print(empresa)
	print(tipo_libro)
	instance = Libro(empresa=empresa, tipo_libro=tipo_libro)
	instance.save()
	return HttpResponseRedirect(instance.get_absolute_url())
def m_libro(request, id=None):
	instance = get_object_or_404(Libro, id=id)
	form = LibroForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print (form.errors)
	context = {
		"title" : "Modificar Libro",
		"instance" : instance,
		"form" : form,
	}
	return render(request, "altas.html", context)
def v_libro(request, id=None):
	instance = get_object_or_404(Libro, id=id)
	list_detalle = Detalle.objects.all().order_by('-fecha').filter(libro=instance)
	imp_x_det={}
	for d in list_detalle:
		importe=d.gravado+d.no_gravado+d.iva21+d.iva105+d.iva_otros+d.rg2126+d.ret_IVA+d.ret_iibb+d.imp_int+d.otros
		imp_x_det[d.id]=importe
	print(imp_x_det)
	# print(list_detalle)


	query = request.GET.get("q")
	if query:
		list_detalle = list_detalle.filter(sucursal__icontains=query)

	paginator = Paginator(list_detalle, 10) # Show 25 DetAna_queryset per page
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
		# "list_detalle": list_detalle,
		"imp_x_det": imp_x_det,
		"instance" : instance,
		"title": "Libro",
	}
	return render(request, "v_libro.html", context)
def l_libro(request):
	
	list_emp=Empresa.objects.all().order_by('-id')
	list_libros=Libro.objects.all()

	#libros
	lib_x_emp={}
	for e in list_emp:
		k=e
		list_lxe=['X', 'X'] #listado de libros por empresa
		for l in list_libros:
			if e == l.empresa:
				if l.tipo_libro == 'V':
					list_lxe[0]=l
				if l.tipo_libro == 'C':
					list_lxe[1]=l
		lib_x_emp[k]=list_lxe	
	print(lib_x_emp)

	context = {
		"object_list_empresa": list_emp,
		"object_dict_libro": lib_x_emp,

		"title": "Listado de Libros"
	}
	return render(request, "l_libro.html", context)
def d_libro(request, id=None):
	instance = get_object_or_404(Libro, id=id)
	instance.delete()
	return redirect("iva:home")

# Detalle 

def a_detalle(request, l=None):
	libro = get_object_or_404(Libro, id=l)
	instance = Detalle(libro=libro)
	#instance.save()
	form = DetalleForm(request.POST or None, instance=instance)
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print (form.errors)
	context = {
		"libro": libro,
		"title" : "Alta de Detalle",
		"form": form,

	}
	return render(request, "altas.html", context)
def m_detalle(request, id=None):
	instance = get_object_or_404(Detalle, id=id)
	form = DetalleForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print (form.errors)
	context = {
		"title" : "Modificar Detalle",
		"instance" : instance,
		"form" : form,
	}
	return render(request, "altas.html", context)
def v_detalle(request, id=None):
	instance = get_object_or_404(Detalle, id=id)
	objeto = DetalleForm(data=model_to_dict(Detalle.objects.get(id=id), exclude=["libro"]))
	context = {
		"instance" : instance,
		"title": "Detalle de Detalle",
		"objeto": objeto,
	}
	return render(request, "v_detalle.html", context)
def l_detalle(request):
	queryset = Detalle.objects.all().order_by('id')
	context = {
		"object_list": queryset,
		"title": "Listado de Detalles"
	}
	return render(request, "l_detalle.html", context)
def d_detalle(request, id=None):
	instance = get_object_or_404(Detalle, id=id)
	id_libro = instance.libro.id
	instance.delete()
	return redirect("iva:v_libro", id=id_libro)
