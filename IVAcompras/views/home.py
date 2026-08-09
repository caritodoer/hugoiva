from cuentas.decorators import require_auth
from django.shortcuts import render
from ..models import Empresa, Libro

@require_auth
def home(request):
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

	context = {
		"object_dict_libro": lib_x_emp,
		"title": "Libros IVA Ventas / Compras",
	}	
	return render(request, "home.html", context)
