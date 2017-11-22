from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, get_user_model, login, logout

User = get_user_model()
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

# inicio reportlab
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.colors import pink, green, brown, white, black, magenta, red
import time
from reportlab.lib.enums import *
from reportlab.lib.pagesizes import letter, A4,landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, TableStyle, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

from django.views.generic import ListView
from reportlab.lib.utils import ImageReader

PAGE_HEIGHT=A4[1]
PAGE_WIDTH=A4[0]
styles = getSampleStyleSheet()

pdfmetrics.registerFont(TTFont('Existence-Light', '../IVA-modal/static/fonts/Existence-Light.ttf'))
pdfmetrics.registerFont(TTFont('Ubuntu-B', '../IVA-modal/static/fonts/ubuntu-font-family-0.83/Ubuntu-B.ttf'))
pdfmetrics.registerFont(TTFont('Ubuntu-L', '../IVA-modal/static/fonts/ubuntu-font-family-0.83/Ubuntu-L.ttf'))
pdfmetrics.registerFont(TTFont('Ubuntu-M', '../IVA-modal/static/fonts/ubuntu-font-family-0.83/Ubuntu-M.ttf'))
pdfmetrics.registerFont(TTFont('Ubuntu-C', '../IVA-modal/static/fonts/ubuntu-font-family-0.83/Ubuntu-C.ttf'))
pdfmetrics.registerFont(TTFont('Ubuntu-R', '../IVA-modal/static/fonts/ubuntu-font-family-0.83/Ubuntu-R.ttf'))

styles.add(ParagraphStyle(name='tit2', alignment=TA_CENTER, fontName = "Ubuntu-M", fontSize = 14))
styles.add(ParagraphStyle(name='tit1', alignment=TA_CENTER, fontName = "Existence-Light", fontSize = 16))
styles.add(ParagraphStyle(name='tit3', alignment=TA_LEFT, fontName = "Ubuntu-L", fontSize = 12))
styles.add(ParagraphStyle(name='tablas', alignment=TA_LEFT, fontName = "Ubuntu-C", fontSize = 11))
styles.add(ParagraphStyle(name='textos', alignment=TA_LEFT, fontName = "Ubuntu-R", fontSize = 10))

tit1 = styles["tit1"]
tit2 = styles["tit2"]
tit3 = styles["tit3"]
tablas = styles["tablas"]
textos = styles["textos"]

LIST_STYLE = TableStyle(
	[('GRID', (0,0), (17, -1), 1, colors.dodgerblue),
	('BACKGROUND', (0,0), (-1, 0), colors.dodgerblue),
	('FONT', (0,0), (-1, -1), 'Ubuntu-C', 10)]
)
# fin reportlab

# Create your views here.
def usuarios(request):
	if not request.user.is_authenticated():
		raise Http404
	queryset = User.objects.all()
	context = {
		
		"object_list": queryset,
		"title": "Usuarios"
	}
	return render(request, "usuarios.html", context)

def exp_empresa(request):
	if not request.user.is_authenticated():
		raise Http404
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
    if not request.user.is_authenticated():
        raise Http404
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
    if not request.user.is_authenticated():
        raise Http404
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
    if not request.user.is_authenticated():
        raise Http404
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
	if not request.user.is_authenticated():
		raise Http404
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
	if not request.user.is_authenticated():
		raise Http404
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
	if not request.user.is_authenticated():
		raise Http404
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
	if not request.user.is_authenticated():
		raise Http404
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
	if not request.user.is_authenticated():
		raise Http404
	instance = get_object_or_404(Empresa, id=id)
	context = {
		"instance" : instance,
		"title": "Detalle de Empresa",
	}
	return render(request, "v_empresa.html", context)
def d_empresa(request, id=None):
	if not request.user.is_authenticated():
		raise Http404
	instance = get_object_or_404(Empresa, id=id)
	instance.delete()
	return redirect("iva:home")

def a_cp_modal(request):
	if not request.user.is_authenticated():
		raise Http404
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
	if not request.user.is_authenticated():
		raise Http404
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
	if not request.user.is_authenticated():
		raise Http404
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
	if not request.user.is_authenticated():
		raise Http404
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
	if not request.user.is_authenticated():
		raise Http404
	instance = get_object_or_404(CliPro, id=id)
	context = {
		"instance" : instance,
		"title": "Detalle de Cliente/Proveedor",
	}
	return render(request, "v_cli_pro.html", context)
def d_cli_pro(request, id=None):
	if not request.user.is_authenticated():
		raise Http404
	instance = get_object_or_404(CliPro, id=id)
	instance.delete()
	return redirect("iva:home")

# Libro 
def i_libro(request, id=None):
	if not request.user.is_authenticated():
		raise Http404
	instance = get_object_or_404(Libro, id=id)
	if instance.tipo_libro == "V":
		tipo_libro="Libro Ventas"
	else:
		tipo_libro="Libro Compras"
	
	list_detalle = Detalle.objects.all().order_by('-fecha').filter(libro=instance)
	desde = request.GET.get("d")
	hasta = request.GET.get("h")
	if desde and hasta:
		list_detalle = list_detalle.filter(fecha__range=(desde, hasta))

		#inicio reportlab
		response = HttpResponse(content_type='application/pdf')
		pdf_name = "libro_%d.pdf" %instance.id
		response['Content-Disposition'] = 'filename=%s; pagesize=landscape(A4)' %pdf_name
		buff = BytesIO()
		title = "Libro_%d" %instance.id
		
		Story = [Spacer(1, 0)]
		style = styles["textos"]
		
		def myFirstPage(canvas, doc):
			canvas.saveState()
			# numeracion de pagina
			canvas.setFont('Ubuntu-R', 8)
			canvas.drawString(inch, 0.75 * inch, "Pagina %d / %s - %s - Periodo: %s - %s" %(doc.page, instance.empresa, tipo_libro, desde, hasta))
			canvas.restoreState()
		def cuerpo(canvas): 
			empresa = Paragraph("""<b>Empresa: </b>"""+instance.empresa.nombre+"""<br/><b>C.U.I.T.: </b>"""+instance.empresa.cuit+"""<br/><b>Propietario: </b>"""+instance.empresa.propietario
				+"""<br/><b>Localidad: </b>"""+instance.empresa.localidad+"""<br/><b>Direccion: </b>"""+instance.empresa.direccion+"""<br/><b>Telefono: </b>"""+instance.empresa.telefono
				+"""<br/><b>Directorio: </b>"""+instance.empresa.directorio, styles["Normal"]) 
			Story.append(empresa)
			Story.append(Spacer(1, 12))

			
			fd=str(desde)
			fh=str(hasta)
			fecha = Paragraph("""<b>Periodo: </b>: Desde: """+fd+""" - Hasta: """+fh, styles["Normal"]) 
			Story.append(fecha)
			Story.append(Spacer(1, 12))

			libro = Paragraph(tipo_libro, tit1) 
			Story.append(libro)
			Story.append(Spacer(1, 20))

			headings = ["Fecha", "TC", "Lt", "Suc", "N°", "Cliente/Proveedo - CUIT", "Gravado", "No Gravado", "IVA 21%", "IVA 10,5%", "IVA Otros", "RG2126", "Ret. IVA", "Ret. IIBB", "Imp. Int.", "Otros", "Total"]
			allregistros = []
			for r in list_detalle:
				registro=[]
				registro.append(r.fecha)
				registro.append(r.tipo_comprobante)
				registro.append(r.letra)
				registro.append(r.sucursal)
				registro.append(r.nfactura)
				registro.append(r.cli_pro.nombre+" - "+r.cli_pro.cuit)
				registro.append(r.gravado)
				registro.append(r.no_gravado)
				registro.append(r.iva21)
				registro.append(r.iva105)
				registro.append(r.iva_otros)
				registro.append(r.rg2126)
				registro.append(r.ret_IVA)
				registro.append(r.ret_iibb)
				registro.append(r.imp_int)
				registro.append(r.otros)
				total=r.gravado+r.no_gravado+r.iva21+r.iva105+r.iva_otros+r.rg2126+r.ret_IVA+r.ret_iibb+r.imp_int+r.otros
				registro.append(total)

				
				allregistros.append(registro)
				#print(allregistros)
			t = Table([headings] + allregistros)
			t.setStyle(LIST_STYLE)
			# print(len(headings))
			# t._argW[0]=1*inch
			# for i in range (0,len(headings)):
			# 	t._argW[i]=0.5*inch
			# # t._argW[3]=5.5*inch
			Story.append(t)
			Story.append(Spacer(1, 12))
			return Story

		Story = cuerpo(canvas)
		doc = SimpleDocTemplate(buff, pagesize=landscape(A4), rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=75)
		#Construimos el documento a partir de los argumentos definidos
		doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myFirstPage)
		response.write(buff.getvalue())
		buff.close()
		return response

	context = {
		# "desde": desde,
		# "hasta": hasta,
		"instance": instance,
		"title": "Imprimir Libro",
	}
	return render(request, "i_libro.html", context)

def a_libro(request, k=None, v=None):
	if not request.user.is_authenticated():
		raise Http404
	empresa = get_object_or_404(Empresa, id=k)
	tipo_libro = v
	print(empresa)
	print(tipo_libro)
	instance = Libro(empresa=empresa, tipo_libro=tipo_libro)
	instance.save()
	return HttpResponseRedirect(instance.get_absolute_url())
def m_libro(request, id=None):
	if not request.user.is_authenticated():
		raise Http404
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
	if not request.user.is_authenticated():
		raise Http404
	instance = get_object_or_404(Libro, id=id)
	list_detalle = Detalle.objects.all().order_by('-fecha').filter(libro=instance)
	imp_x_det={}
	for d in list_detalle:
		importe=d.gravado+d.no_gravado+d.iva21+d.iva105+d.iva_otros+d.rg2126+d.ret_IVA+d.ret_iibb+d.imp_int+d.otros
		imp_x_det[d.id]=importe
	print(imp_x_det)
	# print(list_detalle)


	desde = request.GET.get("d")
	hasta = request.GET.get("h")
	print(desde)
	print(hasta)
	if desde and hasta:
		# list_detalle = list_detalle.filter(sucursal__icontains=query)
		list_detalle = list_detalle.filter(fecha__range=(desde, hasta))
		print(list_detalle)


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
	if not request.user.is_authenticated():
		raise Http404
	
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
	if not request.user.is_authenticated():
		raise Http404
	instance = get_object_or_404(Libro, id=id)
	instance.delete()
	return redirect("iva:home")

# Detalle 

def a_detalle(request, l=None):
	if not request.user.is_authenticated():
		raise Http404
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
	if not request.user.is_authenticated():
		raise Http404
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
	if not request.user.is_authenticated():
		raise Http404
	instance = get_object_or_404(Detalle, id=id)
	objeto = DetalleForm(data=model_to_dict(Detalle.objects.get(id=id), exclude=["libro"]))
	context = {
		"instance" : instance,
		"title": "Detalle de Detalle",
		"objeto": objeto,
	}
	return render(request, "v_detalle.html", context)
def l_detalle(request):
	if not request.user.is_authenticated():
		raise Http404
	queryset = Detalle.objects.all().order_by('id')
	context = {
		"object_list": queryset,
		"title": "Listado de Detalles"
	}
	return render(request, "l_detalle.html", context)
def d_detalle(request, id=None):
	if not request.user.is_authenticated():
		raise Http404
	instance = get_object_or_404(Detalle, id=id)
	id_libro = instance.libro.id
	instance.delete()
	return redirect("iva:v_libro", id=id_libro)
