from django.db import models
from django.core.urlresolvers import reverse 

class Empresa(models.Model):
	nombre = models.CharField(max_length=50)
	propietario = models.CharField(max_length=50)
	cuit = models.CharField("CUIT", max_length=50)
	localidad = models.CharField(max_length=50)
	direccion = models.CharField(max_length=50)
	telefono = models.CharField(max_length=50, null=True, blank=True)
	directorio = models.CharField(max_length=50)

	def get_absolute_url(self):
		return reverse("iva:v_empresa", kwargs={"id":self.id})

	def __str__(self):
		return ('%s - %s')%(self.nombre, self.cuit)

class CliPro(models.Model):
	nombre = models.CharField(max_length=30)
	direccion = models.CharField(max_length=30)
	telefono = models.CharField(max_length=30, null=True, blank=True)
	cuit = models.CharField("CUIT", max_length=30)
	es_cliente = models.BooleanField(default=False)
	es_proveedor = models.BooleanField(default=False)
	iva_choices = (
		('CF', 'Consumidor Final'),
		('I', 'Inscripto'),
		('NI', 'No Inscripto'),
		('M', 'Monotributo'),
		('E', 'Exento'),
		)
	iva = models.CharField("Categoría de IVA", max_length=30, choices=iva_choices)
	obs = models.TextField("Observaciones", null=True, blank=True)

	def get_absolute_url(self):
		return reverse("iva:v_cli_pro", kwargs={"id":self.id})

	def __str__(self):
		return ('%s - %s - %s')%(self.nombre, self.cuit, self.iva)

class Libro(models.Model):
	empresa = models.ForeignKey(Empresa)
	tipo_libro_choices = (
		('V', 'Libro Ventas'),
		('C', 'Libro Compras'),
		) 
	tipo_libro = models.CharField("Tipo de Libro", max_length=1, choices=tipo_libro_choices)

	def get_absolute_url(self):
		return reverse("iva:v_libro", kwargs={"id":self.id})

	def __str__(self):
		return ('%s - %s')%(self.empresa, self.tipo_libro)

class Detalle(models.Model):
	libro = models.ForeignKey(Libro)
	fecha = models.DateField(auto_now=False)
	tipo_comprobante_choices = (
		('F', 'Factura'),
		('ND', 'Nota de Débito'),
		('NC', 'Nota de Crédito'),
		('R', 'Recibo'),
		)
	tipo_comprobante = models.CharField("Tipo de comprobante", max_length=2, choices= tipo_comprobante_choices)
	nfactura = models.CharField(max_length=30)
	cli_pro = models.ForeignKey(CliPro)
	alic = models.IntegerField("Alic.", default=0)
	importe = models.IntegerField("Importe Neto")
	
	ex_iva_insc = models.IntegerField("Exento IVA Insc.", default=0)
	ex_19640 = models.IntegerField("Exento 19640 IVA No Insc", default=0)
	ret = models.IntegerField("Retención Internos", default=0)
	
	def get_absolute_url(self):
		return reverse("iva:v_detalle", kwargs={"id":self.id})

	def __str__(self):
		return ('%s - %s - %s - %s - %s')%(self.libro, self.empresa, self.fecha, self.nfactura, self.importe, self.cli_pro)
