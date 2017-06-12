from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse, Http404

# Create your views here.

# Proveedor

def a_proveedor(request):
	form = ProveedorForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print (form.errors)
	context = {
		"title" : "Alta de Proveedor",
		"form": form,
	}
	return render(request, "a_proveedor.html", context)

def m_proveedor(request, id=None):
	instance = get_object_or_404(Proveedor, id=id)
	form = ProveedorForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print (form.errors)
	context = {
		"title" : "Modificar Proveedor",
		"instance" : instance,
		"form" : form,
	}
	return render(request, "a_proveedor.html", context)

def v_proveedor(request, id=None):
	instance = get_object_or_404(Proveedor, id=id)
	context = {
		"instance" : instance,
		"title": "Detalle de Proveedor",
	}
	return render(request, "v_proveedor.html", context)

# Cliente

def a_cliente(request):
	form = ClienteForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print (form.errors)
	context = {
		"title" : "Alta de Cliente",
		"form": form,
	}
	return render(request, "a_cliente.html", context)

def m_cliente(request, id=None):
	instance = get_object_or_404(Cliente, id=id)
	form = ClienteForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print (form.errors)
	context = {
		"title" : "Modificar Cliente",
		"instance" : instance,
		"form" : form,
	}
	return render(request, "a_cliente.html", context)


def v_cliente(request, id=None):
	instance = get_object_or_404(Cliente, id=id)
	context = {
		"instance" : instance,
		"title": "Detalle de Cliente",
	}
	return render(request, "v_cliente.html", context)

# Libro 

def a_libro(request):
	form = LibroForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print (form.errors)
	context = {
		"title" : "Alta de Libro",
		"form": form,
	}
	return render(request, "a_libro.html", context)

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
	return render(request, "a_libro.html", context)

def v_libro(request, id=None):
	instance = get_object_or_404(Libro, id=id)
	context = {
		"instance" : instance,
		"title": "Detalle de Libro",
	}
	return render(request, "v_libro.html", context)