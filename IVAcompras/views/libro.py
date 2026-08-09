from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from cuentas.decorators import require_auth

from ..models import Libro, Detalle, Empresa
from ..forms import LibroForm

# reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4,landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, TableStyle, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

PAGE_HEIGHT=A4[1]
PAGE_WIDTH=A4[0]
styles = getSampleStyleSheet()

pdfmetrics.registerFont(TTFont('Existence-Light', 'static/fonts/Existence-Light.ttf'))
pdfmetrics.registerFont(TTFont('Ubuntu-B', 'static/fonts/ubuntu-font-family-0.83/Ubuntu-B.ttf'))
pdfmetrics.registerFont(TTFont('Ubuntu-L', 'static/fonts/ubuntu-font-family-0.83/Ubuntu-L.ttf'))
pdfmetrics.registerFont(TTFont('Ubuntu-M', 'static/fonts/ubuntu-font-family-0.83/Ubuntu-M.ttf'))
pdfmetrics.registerFont(TTFont('Ubuntu-C', 'static/fonts/ubuntu-font-family-0.83/Ubuntu-C.ttf'))
pdfmetrics.registerFont(TTFont('Ubuntu-R', 'static/fonts/ubuntu-font-family-0.83/Ubuntu-R.ttf'))

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


@require_auth
def i_dgr(request, id=None):
	instance = get_object_or_404(Libro, id=id)
	if instance.tipo_libro == "V":
		tipo_libro="Libro Ventas"
	else:
		tipo_libro="Libro Compras"
	
	mes = request.GET.get("m")
	anio = request.GET.get("a")
	if mes and anio:
		list_detalle = Detalle.objects.filter(libro=instance, fecha__year=anio, fecha__month=mes)
		

		#inicio reportlab
		response = HttpResponse(content_type='application/pdf')
		pdf_name = "Informe_dgr_%d.pdf" %instance.id
		response['Content-Disposition'] = 'filename=%s; pagesize=A4' %pdf_name
		buff = BytesIO()
		title = "Informe_DGR_%d" %instance.id
		
		Story = [Spacer(1, 0)]
		style = styles["textos"]
		
		def myFirstPage(canvas, doc):
			canvas.saveState()
			# numeracion de pagina
			canvas.setFont('Ubuntu-R', 8)
			canvas.drawString(inch, 0.75 * inch, "Pagina %d / %s - Informe DGR - Periodo: %s - %s" %(doc.page, instance.empresa, mes, anio))
			canvas.restoreState()
		def cuerpo(canvas): 
			titulo = Paragraph("Informe DGR", tit1) 
			Story.append(titulo)
			Story.append(Spacer(1, 30))

			empresa = Paragraph("""<b>Empresa: </b>"""+instance.empresa.nombre+"""<br/><b>C.U.I.T.: </b>"""+instance.empresa.cuit+"""<br/><b>Propietario: </b>"""+instance.empresa.propietario
				+"""<br/><b>Localidad: </b>"""+instance.empresa.localidad+"""<br/><b>Direccion: </b>"""+instance.empresa.direccion+"""<br/><b>Telefono: </b>"""+instance.empresa.telefono
				+"""<br/><b>Directorio: </b>"""+instance.empresa.directorio, styles["Normal"]) 
			Story.append(empresa)
			Story.append(Spacer(1, 12))
			

			fecha = Paragraph("""<b>Periodo: </b>"""+mes+""" - """+anio, styles["Normal"]) 
			Story.append(fecha)
			Story.append(Spacer(1, 12))


			total=0
			for r in list_detalle:
				subtotal=0
				subtotal=r.gravado+r.no_gravado+r.iva21+r.iva105+r.iva_otros+r.rg2126+r.ret_IVA+r.ret_iibb+r.imp_int+r.otros
				total = total+subtotal


			tt=str(total)
			tot = Paragraph("""<b>Total: $</b>"""+tt, styles["Normal"])  
			Story.append(tot)
			
			return Story

		Story = cuerpo(canvas)
		doc = SimpleDocTemplate(buff, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=75)
		#Construimos el documento a partir de los argumentos definidos
		doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myFirstPage)
		response.write(buff.getvalue())
		buff.close()
		return response
	
	context = {
		"instance": instance,
		"title": "Informe DGR",
	}
	return render(request, "i_dgr.html", context)

@require_auth
def i_libro(request, id=None):
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
			libro = Paragraph(tipo_libro, tit1) 
			Story.append(libro)
			Story.append(Spacer(1, 30))

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
			t = Table([headings] + allregistros)
			t.setStyle(LIST_STYLE)
			
            
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
		"instance": instance,
		"title": "Imprimir Libro",
	}
	return render(request, "i_libro.html", context)

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
	else:
		print (form.errors)
	context = {
		"title" : "Modificar Libro",
		"instance" : instance,
		"form" : form,
	}
	return render(request, "altas.html", context)

@require_auth
def v_libro(request, id=None):
	instance = get_object_or_404(Libro, id=id)
	list_detalle = Detalle.objects.all().order_by('-fecha', '-tipo_comprobante', 'letra', '-nfactura').filter(libro=instance)
	imp_x_det={}
	for d in list_detalle:
		importe=d.gravado+d.no_gravado+d.iva21+d.iva105+d.iva_otros+d.rg2126+d.ret_IVA+d.ret_iibb+d.imp_int+d.otros
		imp_x_det[d.id]=importe


	desde = request.GET.get("d")
	hasta = request.GET.get("h")

	if desde and hasta:
		list_detalle = list_detalle.filter(fecha__range=(desde, hasta))


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
		"imp_x_det": imp_x_det,
		"instance" : instance,
		"title": "Libro",
	}
	return render(request, "v_libro.html", context)

@require_auth
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

	context = {
		"object_list_empresa": list_emp,
		"object_dict_libro": lib_x_emp,

		"title": "Listado de Libros"
	}
	return render(request, "l_libro.html", context)

@require_auth
def d_libro(request, id=None):
	instance = get_object_or_404(Libro, id=id)
	instance.delete()
	return redirect("iva:home")
