from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse, Http404

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


# Create your views here.
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
		"title": "Sistema de IVA Ventas / Compras",
	}	
	return render(request, "home.html", context)

# EMPRESA
def a_empresa(request):
	form = EmpresaForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

		
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print (form.errors)
	context = {
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

# Cliente/Proveedor
def a_cli_pro(request):
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
	list_detalle = Detalle.objects.all().order_by('fecha').filter(libro=instance)
	print(list_detalle)

	context = {
		
		
		"instance" : instance,
		"title": "Detalle de Libro",
	}
	return render(request, "v_libro.html", context)

def l_libro(request):
	queryset = Libro.objects.all().order_by('id')
	context = {
		"object_list": queryset,
		"title": "Listado de Libros"
	}
	return render(request, "l_libro.html", context)

def d_libro(request, id=None):
	instance = get_object_or_404(Libro, id=id)
	instance.delete()
	return redirect("iva:home")

# Detalle 

def a_detalle(request):
	form = DetalleForm(request.POST or None)
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print (form.errors)
	context = {
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
	context = {
		"instance" : instance,
		"title": "Detalle de Detalle",
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
	instance.delete()
	return redirect("iva:home")
