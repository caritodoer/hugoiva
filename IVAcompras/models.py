from django.db import models
from django.core.urlresolvers import reverse 

class Proveedor(models.Model):
	razon_social = models.CharField(max_length=30)
	cuit = models.CharField("CUIT", max_length=30)
	nombre_fantasia = models.CharField(max_length=30)
	iva_choices = (
		('RI', 'Responsable Inscripto'),
		('M', 'Monotributista'),
		('E', 'Excento'),
		('CF', 'Consumidor Final'),
		)
	iva = models.CharField("IVA", max_length=30, choices=iva_choices)

	def get_absolute_url(self):
		return reverse("iva:d_proveedor", kwargs={"id":self.id})

	def __str__(self):
		return ('%s - %s - %s')%(self.razon_social, self.cuit, self.iva)

class Cliente (models.Model):
	razon_social = models.CharField("Titular / Razon Social", max_length=30)
	comercio = models.CharField(max_length=30)
	domicilio = models.CharField(max_length=30)
	cuit = models.CharField("CUIT", max_length=30)

	def get_absolute_url(self):
		return reverse("iva:d_cliente", kwargs={"id":self.id})

	def __str__(self):
		return ('%s - %s')%(self.razon_social, self.cuit)

class EncabezadoLibro(models.Model):
	cliente = models.ForeignKey(Cliente)
	mes_choices = (
		('01', 'Enero'),
		('02', 'Febrero'),
		('03', 'Marzo'),
		('04', 'Abril'),
		('05', 'Mayo'),
		('06', 'Junio'),		
		('07', 'Julio'),
		('08', 'Agosto'),
		('09', 'Septiembre'),
		('10', 'Octubre'),
		('11', 'Noviembre'),
		('12', 'Dicembre'),
		)
	mes = models.CharField(max_length=30, choices=mes_choices)
	anio = models.CharField(max_length=4, default=2017)

	def get_absolute_url(self):
		return reverse("iva:d_elibro", kwargs={"id":self.id})

class DetalleLibro(models.Model):
	encabezado = models.ForeignKey(EncabezadoLibro)
	fecha = models.DateField(auto_now=False)
	nfactura = models.CharField(max_length=30)
	tipo = models.CharField(max_length=2, default='C')
	proveedor = models.ForeignKey(Proveedor)
	ing_porcentaje = models.IntegerField("Importe Neto Gravado (%)", default=0)
	ing = models.IntegerField("Importe Neto Gravado", default=0) 
	cng = models.IntegerField("Conceptos No Gravados", default=0)
	op_ex = models.IntegerField("Operaciones Exentas")
	iva_liq = models.IntegerField("IVA Liquidado", default=0)
	iva_rec = models.IntegerField("IVA Recargo N/I", default=0)
	total_fac = models.IntegerField("TOTAL Facturado")
	cred_fisc = models.IntegerField("Cred. Fiscal N/Creditos", default=0)
	ret_perc = models.IntegerField("Retenciones / Percepciones", default=0)

	def get_absolute_url(self):
		return reverse("iva:d_dlibro", kwargs={"id":self.id})
